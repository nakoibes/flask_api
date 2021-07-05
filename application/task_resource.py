from typing import Dict
from werkzeug.exceptions import NotFound
from flask.views import MethodView
from flask import request, jsonify
from werkzeug.exceptions import BadRequest

from application.task import Task, TaskType
from application.task_request import TaskRequest
from application.task_service import TaskService


class TaskResource(MethodView):
    def __init__(self, task_service: TaskService):
        self._task_service = task_service

    def post(self):
        task = parse_request(request.json)
        identifier = self._task_service.make_task(task)
        return jsonify({"id": identifier})

    def get(self, identifier: str):
        task = self._task_service.get_task(identifier)
        if not task:
            raise NotFound(f"Task with identifier {identifier} not found")
        return jsonify(task_presentation(task))


def task_presentation(task: Task):
    if task.status.value == "DONE":
        return {"result": task.result, "status": task.status.value}
    else:
        return {"status": task.status.value}


def parse_request(json_request: Dict[str, str]) -> TaskRequest:
    type_ = json_request.get("type")
    text = json_request.get("text")
    if type_ not in TaskType.__members__.keys():
        raise BadRequest(f"invalid type {type_}")
    if not type_ or not text:
        raise BadRequest("both arguments are required")
    if not isinstance(type_, str) or not isinstance(text, str):
        raise BadRequest(f"expected str but found {type(type_)} and {type(text)}")
    return TaskRequest(TaskType(type_), text)
