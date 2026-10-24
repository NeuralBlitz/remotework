from __future__ import annotations

from pg_anomaly.models import AnomalyAlert, MetricPoint


class MetricSubject:
    def __init__(self) -> None:
        self._observers: list[type[AnomalyObserver]] = []
        self._buffer: list[MetricPoint] = []
        self._max_buffer: int = 1000

    def attach(self, observer: type[AnomalyObserver]) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: type[AnomalyObserver]) -> None:
        self._observers.remove(observer)

    def emit(self, point: MetricPoint) -> list[AnomalyAlert]:
        self._buffer.append(point)
        if len(self._buffer) > self._max_buffer:
            self._buffer = self._buffer[-self._max_buffer :]
        alerts: list[AnomalyAlert] = []
        for obs in self._observers:
            alerts.extend(obs.update(point, self._buffer))
        return alerts

    def get_buffer(self) -> list[MetricPoint]:
        return list(self._buffer)

    def clear_buffer(self) -> None:
        self._buffer.clear()

    @property
    def observer_count(self) -> int:
        return len(self._observers)


from typing import Protocol


class AnomalyObserver(Protocol):
    def update(self, point: MetricPoint, history: list[MetricPoint]) -> list[AnomalyAlert]: ...
