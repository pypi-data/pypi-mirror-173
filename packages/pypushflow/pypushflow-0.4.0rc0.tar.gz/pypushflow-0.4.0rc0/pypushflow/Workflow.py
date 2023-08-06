#
# Copyright (c) European Synchrotron Radiation Facility (ESRF)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__authors__ = ["O. Svensson"]
__license__ = "MIT"
__date__ = "28/05/2019"


import pprint
from typing import Any, Optional
import warnings
from contextlib import contextmanager
from .persistence import db_client
from .logutils import PyPushflowLoggedObject
from .concurrent import get_pool


class Workflow(PyPushflowLoggedObject):
    def __init__(self, name, level=None):
        if level is not None:
            warnings.warn(
                "Use 'pypushflow.logutils.basicConfig(filename=name, level=logging.DEBUG)'",
                DeprecationWarning,
            )
        super().__init__(log_metadata={"workflow": name})
        self.logger.info("\n\nStarting new workflow '%s'\n", name)
        self.name = name
        self.listOnErrorActor = []
        self.db_client = db_client()
        self.db_client.startWorkflow(name)
        self.listActorRef = []
        self._shared_pool = None
        self._stop_exception = False
        self._stop_event = None
        self._pool_options = dict()

    def connectOnError(self, actor):
        self.logger.debug("connect to error handler '%s'", actor.name)
        self.listOnErrorActor.append(actor)

    def triggerOnError(self, inData):
        self.logger.info(
            "triggered due to error with inData =\n %s", pprint.pformat(inData)
        )
        for onErrorActor in self.listOnErrorActor:
            onErrorActor.trigger(inData)

    def getActorPath(self):
        return "/" + self.name

    def addActorRef(self, actorRef):
        self.logger.debug("add reference to actor '%s'", actorRef.name)
        self.listActorRef.append(actorRef)

    def getListActorRef(self):
        return self.listActorRef

    def setStatus(self, status):
        self.db_client.setWorkflowStatus(status)

    def endWorkflow(self, status):
        self.db_client.endWorkflow(status)

    @contextmanager
    def _run_context(
        self,
        shared_pool: bool = False,
        context: Optional[str] = None,
        max_workers: Optional[int] = None,
        pool_type: Optional[str] = None,
        stop_event: Optional[Any] = None,
    ):
        if not shared_pool:
            # A new pool with 1 worker will be created for each asynchronous
            # call and the pool cleanup is done in the callbacks
            self._stop_event = stop_event
            self._stop_exception = None
            self._pool_options = {
                "context": context,
                "max_workers": max_workers,
                "pool_type": pool_type,
            }
            try:
                yield
            except BaseException as e:
                # Make sure PythonActor callbacks do not trigger other tasks
                self._stop_exception = e
                raise
            return
        if self._shared_pool is not None:
            # A pool already exists
            yield
            return

        if max_workers is not None and max_workers <= 0:
            max_workers = sum(actor.pool_resources for actor in self.listActorRef)
        self._pool_options = {
            "context": context,
            "max_workers": max_workers,
            "pool_type": pool_type,
        }
        try:
            self._stop_event = stop_event
            self._stop_exception = None
            with get_pool(pool_type)(**self._pool_options) as pool:
                self._shared_pool = pool
                yield
        except BaseException as e:
            # Make sure PythonActor callbacks do not trigger other tasks
            self._stop_exception = e
            raise
        finally:
            if self._shared_pool is not None:
                self._shared_pool.join()
                self._shared_pool = None

    def run(self, inData, timeout=None, **pool_options):
        with self._run_context(**pool_options):
            self.startActor.trigger(inData)
            self.stopActor.join(timeout=timeout)
            return self.stopActor.outData

    @property
    def pool(self):
        return self._shared_pool

    @property
    def pool_options(self) -> dict:
        return self._pool_options

    @property
    def stop_exception(self) -> Optional[BaseException]:
        if self._stop_exception:
            return self._stop_exception
        if self._stop_event is not None and self._stop_event.is_set():
            return RuntimeError("workflow was interrupted")
