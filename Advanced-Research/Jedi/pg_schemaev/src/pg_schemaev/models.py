"""Migration data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class MigrationStatus(str, Enum):
    PENDING = "pending"
    APPLIED = "applied"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"


@dataclass
class Migration:
    """Represents a single schema migration."""

    migration_id: str
    name: str
    up_sql: str
    down_sql: str
    status: MigrationStatus = MigrationStatus.PENDING
    applied_at: datetime | None = None
    rolled_back_at: datetime | None = None
    checksum: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_applied(self) -> bool:
        return self.status == MigrationStatus.APPLIED

    @property
    def can_rollback(self) -> bool:
        return self.is_applied and bool(self.down_sql)

    def mark_applied(self) -> None:
        self.status = MigrationStatus.APPLIED
        self.applied_at = datetime.now()

    def mark_rolled_back(self) -> None:
        self.status = MigrationStatus.ROLLED_BACK
        self.rolled_back_at = datetime.now()

    def mark_failed(self) -> None:
        self.status = MigrationStatus.FAILED
