from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class PurgeStrategy(Enum):
    DELETE = "delete"
    ARCHIVE_THEN_DELETE = "archive_then_delete"
    ARCHIVE_ONLY = "archive_only"


@dataclass(frozen=True)
class ArchiveConfig:
    archive_table: str
    archive_schema: str = "archive"
    compress: bool = True
    include_indexes: bool = False


@dataclass
class PurgeJob:
    name: str
    from_table: str
    from_schema: str = "public"
    where_older_than: timedelta = timedelta(days=90)
    timestamp_column: str = "created_at"
    archive_config: ArchiveConfig | None = None
    strategy: PurgeStrategy = PurgeStrategy.DELETE
    batch_size: int = 10000
    dry_run: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    extra_conditions: str = ""

    @property
    def qualified_table(self) -> str:
        return f"{self.from_schema}.{self.from_table}"

    @property
    def cutoff_time(self) -> datetime:
        return datetime.now() - self.where_older_than


@dataclass
class PurgeResult:
    job_name: str
    success: bool
    rows_archived: int = 0
    rows_deleted: int = 0
    duration_ms: float = 0.0
    error: str | None = None
    executed_at: datetime = field(default_factory=datetime.now)
    dry_run: bool = False

    @property
    def total_affected(self) -> int:
        return self.rows_archived + self.rows_deleted
