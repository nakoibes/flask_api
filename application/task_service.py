import multiprocessing
import time
import uuid
from typing import Optional
from time import sleep
from application.task import Task, TaskType, TaskStatus
from application.task_repository import MongoDBTaskRepository
from application.task_request import TaskRequest


class TaskService:
    def __init__(self, task_repository):
        self.queue = multiprocessing.Queue()
        self._task_repository = task_repository

    def make_task(self, task_request: TaskRequest) -> str:
        id_ = uuid.uuid4().hex
        text = task_request.text
        type_ = task_request.type
        status = TaskStatus("IN_QUEUE")
        task = Task(id=id_, text=text, type=type_, status=status, timestamp=time.time(), result=None)
        self._task_repository.save_task(task)
        self.queue.put((id_, text, type_))
        return id_

    def get_task(self, id_: str) -> Optional[Task]:
        return self._task_repository.get_by_id(id_)

    def handle_task(self):
        while True:
            # task = self._task_repository.get_task()
            # print(task)
            # task_type, task_text, task_id = task.type.value, task.text, task.id
            # print('++++++++++++++')
            # task_type, task_text, task_id = self._task_repository.get_first_task_in_queue()
            task_id, task_text, task_type = self.queue.get()
            #print(self.queue)
            if task_id:
                self._task_repository.update_status(task_id, TaskStatus("IN_PROGRESS"))
                self._handle_task(task_id, task_type, task_text)
                self._task_repository.update_status(task_id, TaskStatus("DONE"))

    def _handle_task(self, task_id: str, task_type: TaskType, task_text: str):
        if task_type.value == "REVERSE":
            result = self._handle_reverse(task_text)
            self._task_repository.update_result(task_id, result)

        elif task_type.value == "REPLACE":
            result = self._handle_replace(task_text)
            self._task_repository.update_result(task_id, result)

    @staticmethod
    def _handle_reverse(text: str) -> str:
        sleep(2)
        return text[::-1]

    @staticmethod
    def _handle_replace(text: str) -> str:
        text = list(text)
        for index in range(1, len(text)):
            if index % 2 == 1:
                text[index], text[index - 1] = text[index - 1], text[index]
        text = "".join(text)
        sleep(5)
        return text
