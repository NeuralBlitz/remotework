"""Health checking utilities."""
from __future__ import annotations

from .models import HealthStatus

__all__ = ["HealthStatus", "create_status", "aggregate_statuses"]

def create_status(component: str, healthy: bool, message: str = "") -> HealthStatus:
    return HealthStatus(component=component, healthy=healthy, message=message)

def aggregate_statuses(statuses: list[HealthStatus]) -> bool:
    return all(s.healthy for s in statuses)
