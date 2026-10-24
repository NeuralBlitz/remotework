from __future__ import annotations

from feature_tt.models import FeaturePoint, TimeRange
from feature_tt.snapshot import FeatureSnapshot, TemporalJoin


class TemporalFeatureStore:
    def __init__(self) -> None:
        self._points: list[FeaturePoint] = []
        self._join = TemporalJoin()

    def ingest(self, point: FeaturePoint) -> None:
        self._points.append(point)

    def snapshot_at(self, timestamp: int) -> FeatureSnapshot:
        snap = FeatureSnapshot(timestamp)
        for p in sorted(self._points, key=lambda x: x.timestamp):
            snap.add(p)
        self._join.add_snapshot(snap)
        return snap

    def query(self, entity_id: str, feature_name: str, timestamp: int) -> FeaturePoint | None:
        candidates = [
            p
            for p in self._points
            if p.entity_id == entity_id
            and p.feature_name == feature_name
            and p.timestamp <= timestamp
        ]
        if not candidates:
            return None
        return max(candidates, key=lambda p: p.timestamp)

    def history(self, entity_id: str, feature_name: str) -> list[FeaturePoint]:
        return sorted(
            [
                p
                for p in self._points
                if p.entity_id == entity_id and p.feature_name == feature_name
            ],
            key=lambda p: p.timestamp,
        )

    def point_count(self) -> int:
        return len(self._points)

    @property
    def temporal_join(self) -> TemporalJoin:
        return self._join
