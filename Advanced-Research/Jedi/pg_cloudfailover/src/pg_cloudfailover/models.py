from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class FailoverState(Enum):
    PRIMARY = "primary"
    FAILING_OVER = "failing_over"
    STANDBY_PROMOTED = "standby_promoted"
    REBUILDING = "rebuilding"


class FailoverHandler(Protocol):
    def on_enter(self, previous: FailoverState) -> None: ...
    def on_exit(self, next_state: FailoverState) -> None: ...


@dataclass
class FailoverEvent:
    state: FailoverState
    timestamp: float
    message: str
    error: str | None = None
