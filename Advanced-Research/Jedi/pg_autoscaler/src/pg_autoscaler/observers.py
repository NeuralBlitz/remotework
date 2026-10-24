from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import ClusterMetrics, ScaleEvent
from .subject import ClusterObserver


class ScaleUpObserver(ClusterObserver):
    def __init__(self, threshold_cpu: float = 80.0, threshold_conn: float = 0.8) -> None:
        self._threshold_cpu = threshold_cpu
        self._threshold_conn = threshold_conn
        self._events: list[ScaleEvent] = []

    @property
    def events(self) -> list[ScaleEvent]:
        return list(self._events)

    def update(self, metrics: ClusterMetrics) -> None:
        if (
            metrics.cpu_percent > self._threshold_cpu
            or metrics.connection_utilization > self._threshold_conn
        ):
            from .models import ScaleEvent

            new_count = metrics.replica_count + 1
            event = ScaleEvent(
                action="scale_up",
                old_count=metrics.replica_count,
                new_count=new_count,
                reason=f"cpu={metrics.cpu_percent:.1f}%, conn={metrics.connection_utilization:.1%}",
            )
            self._events.append(event)


class ScaleDownObserver(ClusterObserver):
    def __init__(self, threshold_cpu: float = 30.0, threshold_conn: float = 0.3) -> None:
        self._threshold_cpu = threshold_cpu
        self._threshold_conn = threshold_conn
        self._events: list[ScaleEvent] = []
        self._min_replicas = 1

    @property
    def events(self) -> list[ScaleEvent]:
        return list(self._events)

    def set_min_replicas(self, count: int) -> None:
        self._min_replicas = max(1, count)

    def update(self, metrics: ClusterMetrics) -> None:
        if metrics.replica_count <= self._min_replicas:
            return
        if (
            metrics.cpu_percent < self._threshold_cpu
            and metrics.connection_utilization < self._threshold_conn
        ):
            from .models import ScaleEvent

            new_count = max(self._min_replicas, metrics.replica_count - 1)
            event = ScaleEvent(
                action="scale_down",
                old_count=metrics.replica_count,
                new_count=new_count,
                reason=f"cpu={metrics.cpu_percent:.1f}%, conn={metrics.connection_utilization:.1%}",
            )
            self._events.append(event)
