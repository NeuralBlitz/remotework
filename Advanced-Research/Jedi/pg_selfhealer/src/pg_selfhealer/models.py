from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CORRUPT = "corrupt"
    REBUILDING = "rebuilding"


@dataclass
class IndexHealth:
    index_name: str
    table_name: str
    status: HealthStatus
    bloat_pct: float = 0.0
    last_checked: datetime = field(default_factory=datetime.utcnow)
    error_message: str | None = None

    @property
    def needs_rebuild(self) -> bool:
        return self.status == HealthStatus.CORRUPT or self.bloat_pct > 40.0


@dataclass
class RebuildJob:
    index_name: str
    table_name: str
    status: str = "pending"
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error: str | None = None

    def start(self) -> None:
        self.status = "running"
        self.started_at = datetime.utcnow()

    def complete(self) -> None:
        self.status = "completed"
        self.completed_at = datetime.utcnow()

    def fail(self, error: str) -> None:
        self.status = "failed"
        self.error = error
        self.completed_at = datetime.utcnow()
