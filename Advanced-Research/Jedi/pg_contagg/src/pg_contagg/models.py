from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AggregateState(Enum):
    STALE = "stale"
    REFRESHING = "refreshing"
    CURRENT = "current"
    ERROR = "error"


@dataclass(frozen=True)
class RefreshConfig:
    view_name: str
    source_table: str
    refresh_interval: str = "1 hour"
    refresh_lag: str = "1 hour"
    max_refresh_time: str = "10 minutes"
    retry_count: int = 3
    start_offset: str | None = None
    end_offset: str | None = None

    def validate(self) -> bool:
        return bool(self.view_name) and bool(self.source_table)
