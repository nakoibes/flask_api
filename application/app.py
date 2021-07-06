from multiprocessing import Process
from pymongo import MongoClient
from flask import Flask

from application.task_handler import TaskHandler
from application.task_repository import MongoDBTaskRepository
from application.errors import not_found, bad_data, server_failure
from application.task_resource import TaskResource
from application.task_service import TaskService


def create_app():
    app = Flask(__name__)
    mongo_client = MongoClient(host="localhost", port=27017)
    repository = MongoDBTaskRepository(mongo_client.get_database("test_case"))
    task_handler = TaskHandler(MongoDBTaskRepository(mongo_client.get_database("test_case")))
    service = TaskService(repository, task_handler)
    start_listening(task_handler)
    view_func = TaskResource.as_view("tasks", task_service=service)
    app.add_url_rule("/tasks", view_func=view_func)
    app.add_url_rule("/tasks/<identifier>", view_func=view_func)
    app.register_error_handler(404, not_found)
    app.register_error_handler(400, bad_data)
    app.register_error_handler(500, server_failure)
    return app


def start_listening(task_service: TaskHandler) -> None:
    p = Process(target=task_service.handle_task, daemon=True)
    p.start()
