import logging
from contextlib import contextmanager
from typing import Callable, Optional

from .base import BasePool
from .factory import get_pool

logger = logging.getLogger(__name__)


def apply_async(
    fn: Callable,
    callback: Optional[Callable] = None,
    error_callback: Optional[Callable] = None,
    args=tuple(),
    kwargs=None,
    pool: BasePool = None,
    pool_type: Optional[str] = None,
    **pool_options,
):
    """Execute a function in a worker with callbacks for the result."""
    if pool:
        return pool.apply_async(
            fn,
            args=args,
            kwargs=kwargs,
            callback=callback,
            error_callback=error_callback,
        )

    pool_options["max_workers"] = 1
    pool = get_pool(pool_type)(**pool_options)

    if callback is None:

        def _callback(return_value):
            with _cleanup_pool(pool):
                pass

    else:

        def _callback(return_value):
            with _cleanup_pool(pool):
                return callback(return_value)

    if callback is None:

        def _error_callback(exception):
            with _cleanup_pool(pool):
                pass

    else:

        def _error_callback(exception):
            with _cleanup_pool(pool):
                return error_callback(exception)

    future = pool.apply_async(
        fn,
        args=args,
        kwargs=kwargs,
        callback=_callback,
        error_callback=_error_callback,
    )
    pool.close()
    return future


@contextmanager
def _cleanup_pool(pool):
    try:
        yield
    finally:
        try:
            pool.terminate(block=True)
        except RuntimeError as e:
            if str(e) == "cannot join current thread":
                logger.warning(
                    f"Cannot wait for {type(pool).__name__} to terminate in the current thread"
                )
                return
            raise
