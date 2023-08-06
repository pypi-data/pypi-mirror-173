import pytest
from . import utils


@pytest.mark.parametrize("task_name", list(utils.SUCCESS))
def test_callback(task_name):
    if task_name in ["mppool", "bpool"]:
        pytest.skip("pool hangs with gevent")
    with utils.get_pool("gevent")(wait_on_exit_timeout=30) as pool:
        utils.assert_callback(pool, task_name)


@pytest.mark.parametrize("task_name", list(utils.FAILURE))
def test_error_callback(task_name):
    with utils.get_pool("gevent")(wait_on_exit_timeout=30) as pool:
        utils.assert_error_callback(pool, task_name)
