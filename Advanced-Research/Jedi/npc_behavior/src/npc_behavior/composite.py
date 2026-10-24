from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum

from .models import NPCState


class Status(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    RUNNING = "running"


class Node(ABC):
    @abstractmethod
    def tick(self, state: NPCState) -> Status:
        raise NotImplementedError


class SequenceNode(Node):
    def __init__(self, children: list[Node] | None = None) -> None:
        self.children = children or []

    def tick(self, state: NPCState) -> Status:
        for child in self.children:
            result = child.tick(state)
            if result != Status.SUCCESS:
                return result
        return Status.SUCCESS


class SelectorNode(Node):
    def __init__(self, children: list[Node] | None = None) -> None:
        self.children = children or []

    def tick(self, state: NPCState) -> Status:
        for child in self.children:
            result = child.tick(state)
            if result != Status.FAILURE:
                return result
        return Status.FAILURE


class ConditionNode(Node):
    def __init__(self, check: str, value: bool = True) -> None:
        self.check = check
        self.value = value

    def tick(self, state: NPCState) -> Status:
        actual = getattr(state, self.check, None)
        if actual == self.value:
            return Status.SUCCESS
        return Status.FAILURE


class ActionNode(Node):
    def __init__(self, action: str) -> None:
        self.action = action

    def tick(self, state: NPCState) -> Status:
        state.last_action = self.action
        return Status.SUCCESS


class InverterNode(Node):
    def __init__(self, child: Node) -> None:
        self.child = child

    def tick(self, state: NPCState) -> Status:
        result = self.child.tick(state)
        if result == Status.SUCCESS:
            return Status.FAILURE
        if result == Status.FAILURE:
            return Status.SUCCESS
        return result

