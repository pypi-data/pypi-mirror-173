# pypushflow

A task scheduler for cyclic and acyclic graphs

## Install

```bash
python3 -m pip install pypushflow[mx]
```

Use the `mx` option for installation at MX beamlines.

## Run tests

```bash
python3 -m pip install pypushflow[test]
pytest
```

## Getting started

```python
import logging
from pypushflow.Workflow import Workflow
from pypushflow.StopActor import StopActor
from pypushflow.StartActor import StartActor
from pypushflow.PythonActor import PythonActor
from pypushflow.ThreadCounter import ThreadCounter


class MyWorkflow(Workflow):
    def __init__(self, name):
        super().__init__(name, level=logging.DEBUG)
        ctr = ThreadCounter(parent=self)
        self.startActor = StartActor(parent=self, thread_counter=ctr)
        self.pythonActor = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonActorTest.py",
            name="Python Actor Test",
            thread_counter=ctr,
        )
        self.stopActor = StopActor(parent=self, thread_counter=ctr)
        self.startActor.connect(self.pythonActor)
        self.pythonActor.connect(self.stopActor)


testMyWorkflow = MyWorkflow("Test workflow")
inData = {"name": "World"}
outData = testMyWorkflow.run(inData, timeout=15, shared_pool=True, pool_type="process")
assert outData["reply"] == "Hello World!"
```

## Pool types

### Daemonic

A child process can be daemonic or non-daemonic. When a process exits, it attempts to terminate
all of its daemonic child processes (SIGTERM) while it will wait for non-daemonic child processes to finish.
An interrupt (SIGINT) is propagated to both daemonic and non-daemonic child processes.

A daemonic process is not allowed to create child processes. Otherwise a daemonic process would leave its children
orphaned if it gets terminated when its parent process exits.

Create daemonic child processes

* `multiprocessing.Pool` (cannot be used in a daemonic process)
* `billiard.Pool` (can be used in a daemonic process)

Create non-daemonic child processes

* `concurrent.futures.ProcessPoolExecutor`

Create non-daemonic child processes by default (can be daemonic if requested)

* `multiprocessing.Process`
* `billiard.Process`

This can be verified with

```python
python -m pypushflow.concurrent.check_daemonic
```

### Pool types

Pypushflow supports these pools for concurrent execution of workflow tasks

* gevent: pool of greenlets from `gevent`
* thread: pool of threads from the `concurrent.futures` module
* process: pool of non-daemonic processes from the `concurrent.futures` module
* ndprocess: pool of non-daemonic processes from the `concurrent.futures` module
* multiprocessing: pool of daemonic processes from the `multiprocessing` module
* ndmultiprocessing: pool of non-daemonic processes from the `multiprocessing` module
* billiard: pool of daemonic processes from the `billiard` library

The pool type `process` and `ndprocess` are the same, but `ndprocess` uses explicit
non-daemonic processes like `ndmultiprocessing`.

In a gevent-patched environment the default pool type is *gevent* else it is *process*.

### Workflow tasks

* simple: no subprocess
* subprocess: the `subprocess` module
* cfpool: process pool from the `concurrent.futures` module
* mppool: process pool from the `multiprocessing` module
* mpprocess: process from the `multiprocessing` module
* bpool: process pool from the `billiard` library
* bprocess: process from the `billiard` library

### Pool types and workflow tasks compatibility

Workflow tasks that can be used in each pool type (no gevent monkey patching)

* gevent: -
* thread: simple, subprocess, cfpool, mppool, mpprocess, bpool, bprocess
* process: simple, subprocess, cfpool, mppool, mpprocess, bpool (hangs sometimes), bprocess
* ndprocess: simple, subprocess, cfpool, mppool, mpprocess, bpool (hangs sometimes), bprocess
* multiprocessing: simple, subprocess, bpool (hangs sometimes), bprocess
* ndmultiprocessing: simple, subprocess, cfpool, mppool, mpprocess, bpool (hangs sometimes), bprocess
* billiard: simple, subprocess, bpool (hangs sometimes), bprocess

Workflow tasks that can be used in each pool type (with gevent monkey patching)

* gevent: simple, subprocess, cfpool, mpprocess, bprocess
* thread: simple, subprocess, cfpool, mpprocess, bprocess
* process: simple, subprocess, cfpool (not spawn), mpprocess (not spawn), bprocess (not spawn)
* ndprocess: simple, subprocess, cfpool (not spawn), mpprocess (not spawn), bprocess (not spawn)
* multiprocessing: -
* ndmultiprocessing: -
* billiard: -
