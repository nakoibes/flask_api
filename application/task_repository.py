from typing import Optional
from pymongo.database import Database

from application.task import Task, TaskStatus, TaskType


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

    @staticmethod
    def _deserialize_task(raw_task) -> Task:
        return Task(type=TaskType(raw_task["type"]),
                    id=raw_task["id"],
                    text=raw_task["text"],
                    status=TaskStatus(raw_task["status"]),
                    result=raw_task["result"],
                    )

    @staticmethod
    def _task_serialize(task: Task):
        return dict(id=task.id, text=task.text, type=task.type.value, status=task.status.value, result=task.result)

    def delete_all(self):
        self._db.get_collection(self.collection).delete_many({})

    def update_status(self, task_id: str, new_status: TaskStatus) -> None:
        self._db.get_collection(self.collection).update_one({"id": task_id}, {"$set": {"status": new_status.value}})

    def update_result(self, task_id: str, result: str) -> None:
        self._db.get_collection(self.collection).update_one({"id": task_id}, {"$set": {"result": result}})
