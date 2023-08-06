from numbers import Number
import logging
from billiard.pool import Pool as _Pool
from billiard.pool import ApplyResult as Future
from billiard import get_context
from typing import Callable, Optional
from . import base


logger = logging.getLogger(__name__)


class RemoteTraceback(Exception):
    def __init__(self, tb):
        self.tb = tb

    def __str__(self):
        return self.tb


class BProcessPool(base.BasePool):
    """Pool of non-daemonic processes (but they CAN have sub-processes)."""

    def __init__(
        self, context: str = None, max_workers: Optional[int] = None, **kw
    ) -> None:
        kwargs = dict()
        if isinstance(context, str) or None:
            context = get_context(context)
        logger.info(f"pypushflow process pool context: '{type(context).__name__}'")
        kwargs["context"] = context
        if max_workers is not None:
            kwargs["processes"] = max_workers
        self._pool = _Pool(**kwargs)
        super().__init__(**kw)

    def __enter__(self):
        self._pool.__enter__()
        return super().__enter__()

    def close(self):
        self._pool.close()

    def join(self, timeout: Optional[Number] = None):
        try:
            self._pool.join()
        except RuntimeError as e:
            if str(e) != "cannot join current thread":
                raise

    def terminate(self, block: bool = False, timeout: Optional[Number] = None):
        self.close()
        try:
            self._pool.terminate()
        except RuntimeError as e:
            if str(e) != "cannot join current thread":
                raise
        if block:
            self.join(timeout)

    def apply_async(
        self,
        fn: Callable,
        callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
        args=tuple(),
        kwargs=None,
    ) -> Future:
        if kwargs is None:
            kwargs = dict()

        if error_callback is not None:
            org_error_callback = error_callback

            def error_callback(info):
                info.exception.__cause__ = RemoteTraceback(info.traceback)
                return org_error_callback(info.exception)

        return self._pool.apply_async(
            fn, args=args, kwds=kwargs, callback=callback, error_callback=error_callback
        )
