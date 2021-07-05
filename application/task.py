from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TaskType(Enum):
    REVERSE = "REVERSE"
    REPLACE = "REPLACE"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class TaskStatus(Enum):
    IN_QUEUE = "IN_QUEUE"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


@dataclass
class Task:
    id: str
    text: str
    type: TaskType
    status: TaskStatus
    result: Optional[str]
    timestamp: float
