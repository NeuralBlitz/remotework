from __future__ import annotations

from typing import Any

from pg_health.models import HealthStatus, MetricPoint, SystemHealth


class HealthAggregator:
    def __init__(self) -> None:
        self._adapters: list[Any] = []

    def register_adapter(self, adapter: Any) -> None:
        self._adapters.append(adapter)

    def collect_all(self) -> SystemHealth:
        all_metrics: list[MetricPoint] = []
        sources: list[str] = []

        for adapter in self._adapters:
            metrics = adapter.collect()
            all_metrics.extend(metrics)
            sources.append(adapter.source_name)

        overall = self._compute_overall(all_metrics)
        return SystemHealth(
            overall_status=overall,
            metrics=all_metrics,
            sources=sources,
        )

    def _compute_overall(self, metrics: list[MetricPoint]) -> HealthStatus:
        if not metrics:
            return HealthStatus.UNKNOWN
        priority = {
            HealthStatus.CRITICAL: 0,
            HealthStatus.DEGRADED: 1,
            HealthStatus.UNKNOWN: 2,
            HealthStatus.HEALTHY: 3,
        }
        worst = min(metrics, key=lambda m: priority[m.status])
        return worst.status

    @property
    def adapter_count(self) -> int:
        return len(self._adapters)

    def get_critical_metrics(self, system_health: SystemHealth) -> list[MetricPoint]:
        return system_health.metrics_by_status(HealthStatus.CRITICAL)

    def get_degraded_metrics(self, system_health: SystemHealth) -> list[MetricPoint]:
        return system_health.metrics_by_status(HealthStatus.DEGRADED)
