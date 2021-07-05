import multiprocessing
import time

from typing import Optional
from pymongo.database import Database
from pymongo import ASCENDING

from application.task import Task, TaskStatus, TaskType


class TaskRepository():
    task_storage = dict()
    queue_1 = multiprocessing.Queue()  # maxsize=-1

    def save_task(self, task: Task):
        self.task_storage.update({task.id: task})
        self.queue_1.put((task.id, task.text, task.type))

    def get_by_id(self, id_: str) -> Optional[Task]:
        return self.task_storage.get(id_)

    def get_task(self) -> Optional[Task]:
        try:
            return self.queue_1.get()
            # return next(filter(lambda item: item[1].status.value == "IN_QUEUE", self.task_storage.items()))[1]
        except:
            return None

    # def put_task(self, task_id: str, task_type: str, task_result: str) -> Optional[Task]:
    #     try:
    #         return self.queue_2.put((task_id, task_type, task_result))
    #         # return next(filter(lambda item: item[1].status.value == "IN_QUEUE", self.task_storage.items()))[1]
    #     except:
    #         return None

    def update_status(self, task_id: str, new_status: TaskStatus) -> None:
        # print(task_id)
        # print(self.task_storage.get(task_id))
        self.task_storage.get(task_id).status = new_status

    def update_result(self, task_id: str, result: str) -> None:
        self.task_storage.get(task_id).result = result


class MongoDBTaskRepository:
    def __init__(self, db: Database):
        self._db = db
        self.collection = "Tasks"

    def save_task(self, task: Task):
        self._db.get_collection(self.collection).insert_one(self._task_serialize(task))

    def get_by_id(self, id_: str) -> Optional[Task]:
        raw_task = self._db.get_collection(self.collection).find_one({"id": id_})
        if raw_task:
            return self._deserialize_task(raw_task)

    def get_first_task_in_queue(self) -> Optional[
        tuple]:  # TODO метод взять задачу в работу и сделать метод завершить задачу
        tasks = list(
            self._db.get_collection(self.collection).find({"status": TaskStatus.IN_QUEUE.value}).sort("timestamp",
                                                                                                      direction=ASCENDING).limit(
                1))
        if tasks:
            task = self._deserialize_task(tasks[0])
            return task.type, task.text, task.id
        return None, None, None

    @staticmethod
    def _deserialize_task(raw_task) -> Task:
        return Task(type=TaskType(raw_task["type"]),
                    id=raw_task["id"],
                    text=raw_task["text"],
                    status=TaskStatus(raw_task["status"]),
                    result=raw_task["result"],
                    timestamp=raw_task["timestamp"]
                    )

    @staticmethod
    def _task_serialize(task: Task):
        return dict(id=task.id, text=task.text, type=task.type.value, status=task.status.value, result=task.result,
                    timestamp=task.timestamp)

    def delete_all(self):
        self._db.get_collection(self.collection).delete_many({})

    def update_status(self, task_id: str, new_status: TaskStatus) -> None:
        self._db.get_collection(self.collection).update_one({"id": task_id}, {"$set": {"status": new_status.value}})

    def update_result(self, task_id: str, result: str) -> None:
        self._db.get_collection(self.collection).update_one({"id": task_id}, {"$set": {"result": result}})


if __name__ == '__main__':
    from pymongo import MongoClient

    mongo_client = MongoClient(host="localhost", port=27017)
    repo = MongoDBTaskRepository(mongo_client.get_database("test_case"))
    repo.delete_all()
    task = Task(id="123", text="qweqwe", type=TaskType("REVERSE"), status=TaskStatus("IN_QUEUE"), result="321",
                timestamp=time.time())
    repo.save_task(task)
    repo.update_status("123", TaskStatus.IN_PROGRESS)
    # task = Task(id="321", text="ifug", type=TaskType("REVERSE"), status=TaskStatus("IN_QUEUE"), result="123",
    #             timestamp=time.time())
    # repo.save_task(task)
    # task = Task(id="768", text="ifug", type=TaskType("REVERSE"), status=TaskStatus("IN_QUEUE"), result="123",
    #             timestamp=time.time())
    # repo.save_task(task)
    from pprint import pprint

    pprint(repo.get_by_id("123"))
    # pprint(repo.get_first_task_in_queue())
