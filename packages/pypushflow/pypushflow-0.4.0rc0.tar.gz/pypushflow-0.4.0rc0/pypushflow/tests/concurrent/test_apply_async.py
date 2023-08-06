from contextlib import contextmanager
import pytest
from ...concurrent import apply_async
from ...concurrent import factory
from . import utils


def add(a, b):
    return a + b


def error(a, b):
    raise RuntimeError("intentional error")


@pytest.mark.parametrize("manage_pool", [True, False])
@pytest.mark.parametrize("max_workers", [None, 1])
@pytest.mark.parametrize("pool_type", list(factory._POOLS))
@pytest.mark.parametrize("func", [add, error])
def test_apply_async(manage_pool, max_workers, pool_type, func):
    callback_event = utils.Event()
    failed_msg = ""

    def result_callback(return_value):
        nonlocal failed_msg
        try:
            if return_value != 2:
                failed_msg = f"{return_value} != 2"
        finally:
            callback_event.set()

    def error_callback(exception):
        nonlocal failed_msg
        try:
            if not isinstance(exception, RuntimeError):
                failed_msg = f"{exception} is not a RuntimeError"
            elif str(exception) != "intentional error":
                failed_msg = f"'{exception}' != 'intentional error'"
        finally:
            callback_event.set()

    with run_context(
        manage_pool=manage_pool,
        max_workers=max_workers,
        pool_type=pool_type,
        wait_on_exit_timeout=30,
    ) as pool_options:
        apply_async(
            func,
            args=(1, 1),
            callback=result_callback,
            error_callback=error_callback,
            **pool_options,
        )
        callback_event.wait(10)
        assert not failed_msg, failed_msg


@contextmanager
def run_context(manage_pool=True, **pool_options):
    pool_options["wait_on_exit_timeout"] = 30
    pool_cls = utils.get_pool(pool_options["pool_type"])
    if manage_pool:
        pool = None
        try:
            with pool_cls(**pool_options) as pool:
                yield {"pool": pool, **pool_options}
        finally:
            if pool is not None:
                pool.join()
    else:
        yield pool_options
