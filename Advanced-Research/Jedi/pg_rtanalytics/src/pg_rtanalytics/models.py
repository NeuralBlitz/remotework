"""Data models for real-time analytics."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class EventType(str, Enum):
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"


@dataclass(frozen=True)
class NotificationEvent:
    table_name: str
    event_type: EventType
    row_data: dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    channel: str = "default"

    @property
    def is_high_value(self) -> bool:
        amount = self.row_data.get("amount", 0)
        return isinstance(amount, (int, float)) and amount > self.threshold

    threshold: float = 1000.0


@dataclass
class ThresholdConfig:
    min_amount: float = 1000.0
    max_amount: float = 1_000_000.0
    watched_tables: list[str] = field(default_factory=lambda: ["transactions", "orders"])
    channels: list[str] = field(default_factory=lambda: ["analytics"])

    def is_above_threshold(self, value: float) -> bool:
        return self.min_amount < value <= self.max_amount

    def is_watched_table(self, table_name: str) -> bool:
        return table_name in self.watched_tables
