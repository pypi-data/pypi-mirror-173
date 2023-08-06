from threading import Event
import pytest
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from pypushflow.Workflow import Workflow
from pypushflow.StopActor import StopActor
from pypushflow.StartActor import StartActor
from pypushflow.PythonActor import PythonActor
from pypushflow.ThreadCounter import ThreadCounter
from pypushflow.ErrorHandler import ErrorHandler


@pytest.mark.parametrize("sleep_time", [0, 2])
def test_workflow_stop(sleep_time, workflow_cleanup, caplog):
    testWorkflow1 = WorkflowSleep("Test workflow Sleep")
    inData = {"sleep_time": 3}

    with ThreadPoolExecutor() as executor:
        stop_event = Event()
        future = executor.submit(
            testWorkflow1.run,
            inData,
            timeout=15,
            shared_pool=True,
            max_workers=-1,
            stop_event=stop_event,
        )
        if sleep_time:
            sleep(sleep_time)
        stop_event.set()
        result = future.result()
        assert result["WorkflowException"]["errorMessage"] == "workflow was interrupted"
        expected = "[Test workflow Sleep] [<PythonActor> Python Actor Sleep] workflow was interrupted"
        assert any(record[-1] == expected for record in caplog.record_tuples)


class WorkflowSleep(Workflow):
    def __init__(self, name):
        super().__init__(name)
        ctr = ThreadCounter(parent=self)
        self.startActor = StartActor(parent=self, thread_counter=ctr)
        self.errorActor = ErrorHandler(parent=self, thread_counter=ctr)
        self.pythonActor1 = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonActorSleep.py",
            name="Python Actor Sleep",
            thread_counter=ctr,
        )
        self.pythonActor2 = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonActorSleep.py",
            name="Python Actor Sleep",
            thread_counter=ctr,
        )
        self.pythonActor3 = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonActorSleep.py",
            name="Python Actor Sleep",
            thread_counter=ctr,
        )
        self.stopActor = StopActor(parent=self, thread_counter=ctr)
        self.startActor.connect(self.pythonActor1)
        self.pythonActor1.connect(self.pythonActor2)
        self.pythonActor2.connect(self.pythonActor3)
        self.pythonActor3.connect(self.stopActor)
        self.errorActor.connect(self.stopActor)
        self.pythonActor1.connectOnError(self.errorActor)
        self.pythonActor2.connectOnError(self.errorActor)
        self.pythonActor3.connectOnError(self.errorActor)
