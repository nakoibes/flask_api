import time
import uuid
from typing import Optional
from application.task import Task, TaskStatus
from application.task_request import TaskRequest


class TaskService:
    def __init__(self, task_repository, handler):
        self._handler = handler
        self._task_repository = task_repository

    def make_task(self, task_request: TaskRequest) -> str:
        id_ = uuid.uuid4().hex
        text = task_request.text
        type_ = task_request.type
        status = TaskStatus("IN_QUEUE")
        task = Task(id=id_, text=text, type=type_, status=status, timestamp=time.time(), result=None)
        self._task_repository.save_task(task)
        self._handler.put_task((id_, text, type_))
        return id_

    def get_task(self, id_: str) -> Optional[Task]:
        return self._task_repository.get_by_id(id_)
