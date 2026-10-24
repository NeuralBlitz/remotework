from __future__ import annotations

from feature_tt.models import FeaturePoint, TimeRange


class FeatureSnapshot:
    def __init__(self, timestamp: int) -> None:
        self._timestamp = timestamp
        self._features: dict[str, FeaturePoint] = {}

    def add(self, point: FeaturePoint) -> None:
        if point.timestamp <= self._timestamp:
            self._features[point.key()] = point

    def get(self, entity_id: str, feature_name: str) -> FeaturePoint | None:
        return self._features.get(f"{entity_id}:{feature_name}")

    def all_features(self) -> list[FeaturePoint]:
        return list(self._features.values())

    @property
    def timestamp(self) -> int:
        return self._timestamp


class TemporalJoin:
    def __init__(self) -> None:
        self._snapshots: list[FeatureSnapshot] = []

    def add_snapshot(self, snapshot: FeatureSnapshot) -> None:
        self._snapshots.append(snapshot)
        self._snapshots.sort(key=lambda s: s.timestamp)

    def join_at(self, ts: int) -> FeatureSnapshot:
        merged = FeatureSnapshot(ts)
        for snap in self._snapshots:
            if snap.timestamp <= ts:
                for feat in snap.all_features():
                    merged.add(feat)
        return merged

    def range_query(self, time_range: TimeRange) -> list[FeatureSnapshot]:
        return [s for s in self._snapshots if time_range.contains(s.timestamp)]

    def snapshot_count(self) -> int:
        return len(self._snapshots)
