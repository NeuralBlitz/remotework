from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import ClusterMetrics


class ClusterObserver(ABC):
    @abstractmethod
    def update(self, metrics: ClusterMetrics) -> None: ...


class ClusterMetricsSubject:
    def __init__(self) -> None:
        self._observers: list[ClusterObserver] = []
        self._metrics: ClusterMetrics | None = None

    def attach(self, observer: ClusterObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: ClusterObserver) -> None:
        self._observers.remove(observer)

    @property
    def observer_count(self) -> int:
        return len(self._observers)

    def update_metrics(self, metrics: ClusterMetrics) -> None:
        self._metrics = metrics
        self._notify()

    @property
    def metrics(self) -> ClusterMetrics | None:
        return self._metrics

    def _notify(self) -> None:
        if self._metrics is None:
            return
        for observer in self._observers:
            observer.update(self._metrics)
