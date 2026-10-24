from __future__ import annotations

from datetime import datetime
from typing import Protocol

from pg_health.models import HealthStatus, MetricPoint


class HealthAdapter(Protocol):
    def collect(self) -> list[MetricPoint]: ...

    @property
    def source_name(self) -> str: ...


class PgStatAdapter:
    def __init__(
        self,
        active_connections: int = 50,
        max_connections: int = 100,
        idle_connections: int = 20,
        waiting_connections: int = 0,
    ) -> None:
        self.active_connections = active_connections
        self.max_connections = max_connections
        self.idle_connections = idle_connections
        self.waiting_connections = waiting_connections

    @property
    def source_name(self) -> str:
        return "pg_stat_activity"

    def collect(self) -> list[MetricPoint]:
        usage_pct = (self.active_connections / self.max_connections) * 100
        status = HealthStatus.HEALTHY
        if usage_pct >= 90:
            status = HealthStatus.CRITICAL
        elif usage_pct >= 70:
            status = HealthStatus.DEGRADED

        now = datetime.now()
        return [
            MetricPoint(
                name="active_connections",
                value=float(self.active_connections),
                unit="connections",
                source=self.source_name,
                timestamp=now,
                status=status,
                threshold_warning=float(self.max_connections * 0.7),
                threshold_critical=float(self.max_connections * 0.9),
            ),
            MetricPoint(
                name="connection_usage_pct",
                value=usage_pct,
                unit="percent",
                source=self.source_name,
                timestamp=now,
                status=status,
                threshold_warning=70.0,
                threshold_critical=90.0,
            ),
            MetricPoint(
                name="waiting_connections",
                value=float(self.waiting_connections),
                unit="connections",
                source=self.source_name,
                timestamp=now,
                status=HealthStatus.CRITICAL
                if self.waiting_connections > 0
                else HealthStatus.HEALTHY,
            ),
        ]


class ReplicationLagAdapter:
    def __init__(self, lag_bytes: float = 0, lag_seconds: float = 0) -> None:
        self.lag_bytes = lag_bytes
        self.lag_seconds = lag_seconds

    @property
    def source_name(self) -> str:
        return "pg_stat_replication"

    def collect(self) -> list[MetricPoint]:
        lag_status = HealthStatus.HEALTHY
        if self.lag_seconds >= 30:
            lag_status = HealthStatus.CRITICAL
        elif self.lag_seconds >= 5:
            lag_status = HealthStatus.DEGRADED

        now = datetime.now()
        return [
            MetricPoint(
                name="replication_lag_seconds",
                value=self.lag_seconds,
                unit="seconds",
                source=self.source_name,
                timestamp=now,
                status=lag_status,
                threshold_warning=5.0,
                threshold_critical=30.0,
            ),
            MetricPoint(
                name="replication_lag_bytes",
                value=self.lag_bytes,
                unit="bytes",
                source=self.source_name,
                timestamp=now,
                status=lag_status,
            ),
        ]


class SystemMetricAdapter:
    def __init__(
        self,
        cpu_percent: float = 10.0,
        memory_percent: float = 50.0,
        disk_usage_percent: float = 40.0,
        iops: float = 1000.0,
    ) -> None:
        self.cpu_percent = cpu_percent
        self.memory_percent = memory_percent
        self.disk_usage_percent = disk_usage_percent
        self.iops = iops

    @property
    def source_name(self) -> str:
        return "os_metrics"

    def collect(self) -> list[MetricPoint]:
        now = datetime.now()

        def _status(value: float, warn: float, crit: float) -> HealthStatus:
            if value >= crit:
                return HealthStatus.CRITICAL
            if value >= warn:
                return HealthStatus.DEGRADED
            return HealthStatus.HEALTHY

        return [
            MetricPoint(
                name="cpu_percent",
                value=self.cpu_percent,
                unit="percent",
                source=self.source_name,
                timestamp=now,
                status=_status(self.cpu_percent, 70, 90),
                threshold_warning=70.0,
                threshold_critical=90.0,
            ),
            MetricPoint(
                name="memory_percent",
                value=self.memory_percent,
                unit="percent",
                source=self.source_name,
                timestamp=now,
                status=_status(self.memory_percent, 75, 95),
                threshold_warning=75.0,
                threshold_critical=95.0,
            ),
            MetricPoint(
                name="disk_usage_percent",
                value=self.disk_usage_percent,
                unit="percent",
                source=self.source_name,
                timestamp=now,
                status=_status(self.disk_usage_percent, 80, 95),
                threshold_warning=80.0,
                threshold_critical=95.0,
            ),
        ]
