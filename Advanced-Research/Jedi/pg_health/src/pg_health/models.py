from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class MetricPoint:
    name: str
    value: float
    unit: str
    source: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: HealthStatus = HealthStatus.HEALTHY
    threshold_warning: float | None = None
    threshold_critical: float | None = None


@dataclass
class SystemHealth:
    overall_status: HealthStatus
    metrics: list[MetricPoint]
    checked_at: datetime = field(default_factory=datetime.now)
    sources: list[str] = field(default_factory=list)

    @property
    def is_healthy(self) -> bool:
        return self.overall_status == HealthStatus.HEALTHY

    def metrics_by_status(self, status: HealthStatus) -> list[MetricPoint]:
        return [m for m in self.metrics if m.status == status]

    def worst_status(self) -> HealthStatus:
        priority = {
            HealthStatus.CRITICAL: 0,
            HealthStatus.DEGRADED: 1,
            HealthStatus.UNKNOWN: 2,
            HealthStatus.HEALTHY: 3,
        }
        if not self.metrics:
            return HealthStatus.UNKNOWN
        return min(self.metrics, key=lambda m: priority[m.status]).status
