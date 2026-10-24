from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ClusterStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    OVERLOADED = "overloaded"


@dataclass
class ClusterMetrics:
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    connections: int = 0
    max_connections: int = 100
    qps: float = 0.0
    replica_count: int = 1

    @property
    def connection_utilization(self) -> float:
        if self.max_connections == 0:
            return 0.0
        return self.connections / self.max_connections

    @property
    def status(self) -> ClusterStatus:
        if self.cpu_percent > 90 or self.connection_utilization > 0.9:
            return ClusterStatus.OVERLOADED
        if self.cpu_percent > 70 or self.connection_utilization > 0.7:
            return ClusterStatus.DEGRADED
        return ClusterStatus.HEALTHY


@dataclass
class ScaleEvent:
    action: str
    old_count: int
    new_count: int
    reason: str
