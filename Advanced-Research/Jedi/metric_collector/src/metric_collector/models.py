from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Metric:
    name: str
    value: float
    labels: dict[str, str]

@dataclass
class MetricSeries:
    metrics: list[Metric] = field(default_factory=list)
