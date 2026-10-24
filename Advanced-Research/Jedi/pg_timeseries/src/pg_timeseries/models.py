from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CompressionPolicy(Enum):
    NEVER = "never"
    AFTER_7_DAYS = "after_7_days"
    AFTER_30_DAYS = "after_30_days"
    CUSTOM = "custom"


@dataclass(frozen=True)
class HypertableConfig:
    table_name: str
    time_column: str
    chunk_interval: str = "1 day"
    retention_period: str | None = None
    compression_policy: CompressionPolicy = CompressionPolicy.AFTER_7_DAYS

    def validate(self) -> bool:
        return bool(self.table_name) and bool(self.time_column)


@dataclass(frozen=True)
class ChunkInfo:
    chunk_name: str
    hypertable_name: str
    range_start: datetime
    range_end: datetime
    is_compressed: bool = False
    size_bytes: int = 0

    @property
    def duration_days(self) -> float:
        return (self.range_end - self.range_start).total_seconds() / 86400


@dataclass(frozen=True)
class AggregateQuery:
    name: str
    source_table: str
    time_bucket_interval: str
    aggregate_columns: list[str] = field(default_factory=list)
    refresh_interval: str = "1 hour"
    refresh_lag: str = "1 hour"

    def sql_definition(self) -> str:
        cols = ", ".join(self.aggregate_columns) if self.aggregate_columns else "*"
        return (
            f"SELECT time_bucket('{self.time_bucket_interval}', time) AS bucket, {cols} "
            f"FROM {self.source_table} GROUP BY bucket"
        )
