from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"


@dataclass
class Metric:
    name: str
    metric_type: MetricType
    value: float = 0.0
    labels: dict[str, str] = field(default_factory=dict)
    help_text: str = ""


class MetricsCollector:
    def __init__(self) -> None:
        self._metrics: dict[str, Metric] = {}

    def register(
        self,
        name: str,
        metric_type: MetricType,
        help_text: str = "",
        labels: dict[str, str] | None = None,
    ) -> Metric:
        if name in self._metrics:
            raise ValueError(f"Metric {name!r} already registered")
        metric = Metric(
            name=name, metric_type=metric_type, help_text=help_text, labels=labels or {}
        )
        self._metrics[name] = metric
        return metric

    def get(self, name: str) -> Metric:
        if name not in self._metrics:
            raise KeyError(f"Metric {name!r} not found")
        return self._metrics[name]

    def increment(self, name: str, amount: float = 1.0) -> None:
        metric = self.get(name)
        if metric.metric_type == MetricType.COUNTER:
            metric.value += amount
        else:
            metric.value += amount

    def set_gauge(self, name: str, value: float) -> None:
        metric = self.get(name)
        metric.value = value

    def observe(self, name: str, value: float) -> None:
        metric = self.get(name)
        metric.value = value

    def reset(self, name: str) -> None:
        self.get(name).value = 0.0

    def get_all(self) -> list[Metric]:
        return list(self._metrics.values())

    @property
    def metric_count(self) -> int:
        return len(self._metrics)
