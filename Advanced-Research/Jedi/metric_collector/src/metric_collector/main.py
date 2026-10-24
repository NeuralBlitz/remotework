"""Metric collection utilities."""
from __future__ import annotations

from .models import Metric, MetricSeries

__all__ = ["Metric", "MetricSeries", "create_metric", "create_series", "get_total"]

def create_metric(name: str, value: float, labels: dict[str, str] | None = None) -> Metric:
    return Metric(name=name, value=value, labels=labels or {})

def create_series(metrics: list[Metric]) -> MetricSeries:
    return MetricSeries(metrics=metrics)

def get_total(series: MetricSeries) -> float:
    return sum(m.value for m in series.metrics)
