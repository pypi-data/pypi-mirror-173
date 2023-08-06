import pytest
from . import utils
from ..conftest import gevent_patched
from multiprocessing import get_all_start_methods


@pytest.mark.parametrize("task_name", list(utils.SUCCESS))
@pytest.mark.parametrize("context", get_all_start_methods())
def test_callback(task_name, context):
    if gevent_patched():
        if task_name in ["mppool", "bpool"]:
            pytest.skip("pool hangs with gevent")
        if context == "spawn":
            pytest.skip("spawn hangs with gevent")
    else:
        if task_name in ["bpool"]:
            pytest.skip("hangs sometimes")
    with utils.get_pool("ndprocess")(context=context, wait_on_exit_timeout=30) as pool:
        utils.assert_callback(pool, task_name)


@pytest.mark.parametrize("task_name", list(utils.FAILURE))
@pytest.mark.parametrize("context", get_all_start_methods())
def test_error_callback(task_name, context):
    if gevent_patched():
        if context == "spawn":
            pytest.skip("spawn hangs with gevent")
    with utils.get_pool("ndprocess")(context=context, wait_on_exit_timeout=30) as pool:
        utils.assert_error_callback(pool, task_name)
