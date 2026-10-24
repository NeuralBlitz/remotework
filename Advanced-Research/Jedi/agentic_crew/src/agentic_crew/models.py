from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class AgentRole(Enum):
    WORKER = auto()
    MANAGER = auto()
    EXECUTIVE = auto()


@dataclass
class Task:
    description: str
    priority: int = 0
    assigned_to: str = ""
    completed: bool = False

    def mark_completed(self) -> None:
        self.completed = True


@dataclass
class TaskResult:
    task: Task
    output: str
    success: bool
    agent_name: str
    sub_results: list[TaskResult] = field(default_factory=list)
