from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TimeRange:
    start_ts: int = 0
    end_ts: int = 0

    def contains(self, ts: int) -> bool:
        return self.start_ts <= ts <= self.end_ts

    def overlaps(self, other: TimeRange) -> bool:
        return self.start_ts <= other.end_ts and other.start_ts <= self.end_ts

    def duration(self) -> int:
        return self.end_ts - self.start_ts


@dataclass
class FeaturePoint:
    entity_id: str = ""
    feature_name: str = ""
    value: float = 0.0
    timestamp: int = 0
    version: int = 1

    def key(self) -> str:
        return f"{self.entity_id}:{self.feature_name}"
