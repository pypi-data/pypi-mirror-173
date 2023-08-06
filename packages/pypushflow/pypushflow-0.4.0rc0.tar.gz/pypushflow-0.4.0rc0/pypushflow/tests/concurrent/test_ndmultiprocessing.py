import pytest
from . import utils
from multiprocessing import get_all_start_methods

CONTEXTS = [None] + get_all_start_methods()


@pytest.mark.parametrize("task_name", list(utils.SUCCESS))
@pytest.mark.parametrize("context", CONTEXTS)
def test_callback(task_name, context, skip_when_gevent):
    if task_name in ["bpool"]:
        pytest.skip("hangs sometimes")
    with utils.get_pool("ndmultiprocessing")(context=context) as pool:
        utils.assert_callback(pool, task_name)


@pytest.mark.parametrize("task_name", list(utils.FAILURE))
@pytest.mark.parametrize("context", CONTEXTS)
def test_error_callback(task_name, context, skip_when_gevent):
    with utils.get_pool("ndmultiprocessing")(context=context) as pool:
        utils.assert_error_callback(pool, task_name)
