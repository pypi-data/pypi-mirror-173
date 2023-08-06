import pytest
from . import utils
from multiprocessing import get_all_start_methods

CONTEXTS = [None] + get_all_start_methods()


@pytest.mark.parametrize("task_name", list(utils.SUCCESS))
@pytest.mark.parametrize("context", CONTEXTS)
def test_callback(task_name, context, skip_when_gevent):
    with utils.get_pool("multiprocessing")(
        context=context, wait_on_exit_timeout=30
    ) as pool:
        if task_name in ["mppool", "mpprocess", "cfpool"]:
            with pytest.raises(
                AssertionError,
                match="daemonic processes are not allowed to have children",
            ):
                utils.assert_callback(pool, task_name)
            pytest.skip("daemonic processes are not allowed to have children")
        elif task_name in ["bpool"]:
            pytest.skip("hangs sometimes")
        else:
            utils.assert_callback(pool, task_name)


@pytest.mark.parametrize("task_name", list(utils.FAILURE))
@pytest.mark.parametrize("context", CONTEXTS)
def test_error_callback(task_name, context, skip_when_gevent):
    with utils.get_pool("multiprocessing")(
        context=context, wait_on_exit_timeout=30
    ) as pool:
        utils.assert_error_callback(pool, task_name)
