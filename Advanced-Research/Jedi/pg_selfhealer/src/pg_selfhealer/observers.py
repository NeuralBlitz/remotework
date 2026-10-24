from __future__ import annotations

from abc import ABC, abstractmethod

from pg_selfhealer.models import IndexHealth


class IndexObserver(ABC):
    @abstractmethod
    def on_health_check(self, health: IndexHealth) -> None: ...

    @abstractmethod
    def on_corruption_detected(self, health: IndexHealth) -> None: ...


class CorruptionObserver(IndexObserver):
    def __init__(self) -> None:
        self._corruptions: list[IndexHealth] = []

    @property
    def corruptions(self) -> list[IndexHealth]:
        return list(self._corruptions)

    def on_health_check(self, health: IndexHealth) -> None:
        pass

    def on_corruption_detected(self, health: IndexHealth) -> None:
        self._corruptions.append(health)

    def clear(self) -> None:
        self._corruptions.clear()


class RebuildObserver(IndexObserver):
    def __init__(self) -> None:
        self._rebuilds_triggered: list[str] = []

    @property
    def rebuilds_triggered(self) -> list[str]:
        return list(self._rebuilds_triggered)

    def on_health_check(self, health: IndexHealth) -> None:
        if health.needs_rebuild:
            self._rebuilds_triggered.append(health.index_name)

    def on_corruption_detected(self, health: IndexHealth) -> None:
        self._rebuilds_triggered.append(health.index_name)
