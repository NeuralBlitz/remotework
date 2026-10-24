from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(frozen=True)
class MetricPoint:
    name: str
    value: float
    timestamp: datetime
    tags: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Metric name cannot be empty")


@dataclass(frozen=True)
class AnomalyAlert:
    metric_name: str
    point: MetricPoint
    severity: AlertSeverity
    score: float
    message: str
    threshold: float

    @property
    def is_critical(self) -> bool:
        return self.severity == AlertSeverity.CRITICAL
