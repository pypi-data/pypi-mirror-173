from numbers import Number
from typing import Callable, Optional


class BasePool:
    def __init__(
        self,
        wait_on_exit: bool = True,
        wait_on_exit_timeout: Optional[Number] = None,
        **_
    ) -> None:
        self._wait_on_exit = wait_on_exit
        self._wait_on_exit_timeout = wait_on_exit_timeout

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate(block=self._wait_on_exit, timeout=self._wait_on_exit_timeout)

    def close(self):
        """Prevents any more tasks from being submitted to the pool."""
        raise NotImplementedError

    def join(self, timeout: Optional[Number] = None):
        """Wait for the workers to exit."""
        raise NotImplementedError

    def terminate(self, block: bool = False, timeout: Optional[Number] = None):
        """Stops the workers immediately without completing outstanding work."""
        raise NotImplementedError

    def apply_async(
        self,
        fn: Callable,
        callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
        args=tuple(),
        kwargs=None,
    ):
        raise NotImplementedError
