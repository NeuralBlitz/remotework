from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Resolution(Enum):
    MINUTE = "minute"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class DownsampleConfig:
    source_table: str
    target_table: str
    resolution: Resolution
    aggregation: str = "avg"
    retention_days: int = 90
    batch_size: int = 10000

    def validate(self) -> bool:
        return bool(
            self.source_table and self.target_table and self.source_table != self.target_table
        )
