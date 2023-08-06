from numbers import Number
import logging
import sys
from concurrent.futures import ProcessPoolExecutor, Future
from multiprocessing import get_context
from multiprocessing import set_start_method
from typing import Callable, Optional
from . import base

logger = logging.getLogger(__name__)


class ProcessPool(base.BasePool):
    """Pool of non-daemonic processes (they can have sub-processes)."""

    def __init__(
        self, context: str = None, max_workers: Optional[int] = None, **kw
    ) -> None:
        kwargs = dict()

        if sys.version_info >= (3, 7):
            if isinstance(context, str) or None:
                context = get_context(context)
            logger.info(f"pypushflow process pool context: '{type(context).__name__}'")
            kwargs["mp_context"] = context
        else:
            logger.info(f"pypushflow process pool context: '{context}'")
            assert isinstance(context, str) or context is None
            set_start_method(context, force=True)
        if max_workers is not None:
            kwargs["max_workers"] = max_workers
        self._pool = ProcessPoolExecutor(**kwargs)
        self._closed = False
        super().__init__(**kw)

    def __enter__(self):
        self._pool.__enter__()
        return super().__enter__()

    def close(self):
        self._closed = True

    def join(self, timeout: Optional[Number] = None):
        pass

    def terminate(self, block: bool = False, timeout: Optional[Number] = None):
        self.close()
        self._pool.shutdown(wait=block)

    def apply_async(
        self,
        fn: Callable,
        callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
        args=tuple(),
        kwargs=None,
    ) -> Future:
        if self._closed:
            raise RuntimeError("the pool is closed")

        def cb(future):
            try:
                result = future.result()
            except Exception as e:
                if error_callback is not None:
                    error_callback(e)
            else:
                if callback is not None:
                    callback(result)

        if kwargs is None:
            kwargs = dict()
        future = self._pool.submit(fn, *args, **kwargs)
        future.add_done_callback(cb)
        return future
