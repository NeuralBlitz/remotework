from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class BackfillStrategy(Enum):
    BATCH = "batch"
    STREAMING = "streaming"
    HYBRID = "hybrid"


class BackfillStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class BackfillJob:
    job_id: str
    table_name: str
    feature_column: str
    source_columns: list[str] = field(default_factory=list)
    strategy: BackfillStrategy = BackfillStrategy.BATCH
    batch_size: int = 1000
    max_rows: int | None = None

    def validate(self) -> bool:
        return bool(self.job_id) and bool(self.table_name) and bool(self.feature_column)


@dataclass
class BackfillConfig:
    connection_string: str = "postgresql://localhost:5432/db"
    parallel_workers: int = 4
    checkpoint_interval: int = 5000
    retry_attempts: int = 3
    timeout_seconds: int = 3600
    dry_run: bool = False

    def validate(self) -> bool:
        return bool(self.connection_string) and self.parallel_workers > 0


@dataclass
class BackfillProgress:
    job_id: str
    status: BackfillStatus = BackfillStatus.PENDING
    rows_processed: int = 0
    rows_total: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def percentage(self) -> float:
        if self.rows_total == 0:
            return 0.0
        return min(100.0, (self.rows_processed / self.rows_total) * 100)
