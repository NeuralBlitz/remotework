from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class RecoveryType(str, Enum):
    FULL = "full"
    INCREMENTAL = "incremental"
    POINT_IN_TIME = "point_in_time"


@dataclass
class RecoveryPoint:
    id: str
    timestamp: datetime
    recovery_type: RecoveryType
    source_backup: str
    lsn: str = ""
    verified: bool = False
    metadata: dict[str, str] = field(default_factory=dict)


class RecoveryManager:
    def __init__(self) -> None:
        self._recovery_points: dict[str, RecoveryPoint] = {}
        self._operations: list[dict[str, object]] = []

    def add_recovery_point(self, point: RecoveryPoint) -> None:
        if point.id in self._recovery_points:
            raise ValueError(f"Recovery point {point.id!r} already exists")
        self._recovery_points[point.id] = point

    def get_recovery_point(self, point_id: str) -> RecoveryPoint:
        if point_id not in self._recovery_points:
            raise KeyError(f"Recovery point {point_id!r} not found")
        return self._recovery_points[point_id]

    def list_recovery_points(self, source_backup: str | None = None) -> list[RecoveryPoint]:
        points = list(self._recovery_points.values())
        if source_backup:
            points = [p for p in points if p.source_backup == source_backup]
        return sorted(points, key=lambda p: p.timestamp)

    def verify_recovery_point(self, point_id: str) -> bool:
        point = self.get_recovery_point(point_id)
        point.verified = True
        return True

    def get_latest_recovery_point(self) -> RecoveryPoint | None:
        if not self._recovery_points:
            return None
        return max(self._recovery_points.values(), key=lambda p: p.timestamp)

    def recover(self, point_id: str) -> dict[str, object]:
        point = self.get_recovery_point(point_id)
        op = {
            "point_id": point_id,
            "timestamp": datetime.now(timezone.utc),
            "status": "completed",
        }
        self._operations.append(op)
        return op

    @property
    def recovery_point_count(self) -> int:
        return len(self._recovery_points)

    @property
    def operation_count(self) -> int:
        return len(self._operations)
