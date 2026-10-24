from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from agentic_crew.models import AgentRole, Task, TaskResult


class AgentNode(ABC):
    """Composite pattern: leaf and manager share this interface."""

    def __init__(self, name: str, role: AgentRole) -> None:
        self.name = name
        self.role = role

    @abstractmethod
    def execute(self, task: Task) -> TaskResult: ...

    @abstractmethod
    def count(self) -> int: ...


class WorkerAgent(AgentNode):
    """Leaf node that performs tasks directly."""

    def __init__(self, name: str, specialization: str = "") -> None:
        super().__init__(name, AgentRole.WORKER)
        self.specialization = specialization

    def execute(self, task: Task) -> TaskResult:
        task.mark_completed()
        return TaskResult(
            task=task,
            output=f"Worker {self.name} completed: {task.description}",
            success=True,
            agent_name=self.name,
        )

    def count(self) -> int:
        return 1


class ManagerAgent(AgentNode):
    """Composite node that delegates to children."""

    def __init__(self, name: str, role: AgentRole = AgentRole.MANAGER) -> None:
        super().__init__(name, role)
        self._children: list[AgentNode] = []

    def add(self, node: AgentNode) -> None:
        self._children.append(node)

    def remove(self, node: AgentNode) -> None:
        self._children.remove(node)

    @property
    def children(self) -> list[AgentNode]:
        return list(self._children)

    def execute(self, task: Task) -> TaskResult:
        sub_results: list[TaskResult] = []
        for child in self._children:
            sub_task = Task(description=task.description, priority=task.priority)
            result = child.execute(sub_task)
            sub_results.append(result)
        task.mark_completed()
        return TaskResult(
            task=task,
            output=f"Manager {self.name} coordinated {len(sub_results)} subtasks",
            success=all(r.success for r in sub_results),
            agent_name=self.name,
            sub_results=sub_results,
        )

    def count(self) -> int:
        return 1 + sum(child.count() for child in self._children)


class AgentSwarm:
    """Top-level container for the agent hierarchy."""

    def __init__(self, root: ManagerAgent) -> None:
        self.root = root

    def run(self, task: Task) -> TaskResult:
        return self.root.execute(task)

    def agent_count(self) -> int:
        return self.root.count()
