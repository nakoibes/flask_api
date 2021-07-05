from dataclasses import dataclass

from application.task import TaskType


@dataclass(frozen=True)
class TaskRequest:
    type: TaskType
    text: str