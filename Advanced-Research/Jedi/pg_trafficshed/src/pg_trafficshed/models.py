from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class QueryRequest:
    sql: str
    database: str
    priority: int = 0
    timeout_ms: float = 5000.0


@dataclass
class QueryResponse:
    success: bool
    rows: list[dict[str, object]] = field(default_factory=list)
    error: str | None = None
    duration_ms: float = 0.0
    rejected: bool = False


@dataclass
class ShedderStats:
    total_requests: int = 0
    accepted: int = 0
    rejected: int = 0
    circuit_trips: int = 0


class QueryHandler(Protocol):
    def handle(self, request: QueryRequest) -> QueryResponse: ...
