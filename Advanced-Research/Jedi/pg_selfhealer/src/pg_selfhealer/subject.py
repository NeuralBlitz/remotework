from __future__ import annotations

from pg_selfhealer.models import HealthStatus, IndexHealth, RebuildJob
from pg_selfhealer.observers import IndexObserver


class IndexHealthMonitor:
    def __init__(self) -> None:
        self._observers: list[IndexObserver] = []
        self._indexes: dict[str, IndexHealth] = {}
        self._jobs: list[RebuildJob] = []

    def attach(self, observer: IndexObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IndexObserver) -> None:
        self._observers.remove(observer)

    def register_index(self, health: IndexHealth) -> None:
        self._indexes[health.index_name] = health

    def check_health(self, index_name: str) -> IndexHealth:
        health = self._indexes.get(index_name)
        if health is None:
            raise KeyError(f"Index {index_name} not registered")
        for obs in self._observers:
            obs.on_health_check(health)
        if health.status == HealthStatus.CORRUPT:
            self._notify_corruption(health)
        return health

    def check_all(self) -> list[IndexHealth]:
        results: list[IndexHealth] = []
        for name in self._indexes:
            results.append(self.check_health(name))
        return results

    def _notify_corruption(self, health: IndexHealth) -> None:
        for obs in self._observers:
            obs.on_corruption_detected(health)

    def trigger_rebuild(self, index_name: str) -> RebuildJob:
        health = self._indexes.get(index_name)
        if health is None:
            raise KeyError(f"Index {index_name} not registered")
        job = RebuildJob(index_name=index_name, table_name=health.table_name)
        job.start()
        health.status = HealthStatus.REBUILDING
        self._jobs.append(job)
        return job

    def complete_rebuild(self, job: RebuildJob) -> None:
        job.complete()
        health = self._indexes.get(job.index_name)
        if health:
            health.status = HealthStatus.HEALTHY
            health.bloat_pct = 0.0

    @property
    def jobs(self) -> list[RebuildJob]:
        return list(self._jobs)

    @property
    def indexes(self) -> dict[str, IndexHealth]:
        return dict(self._indexes)
