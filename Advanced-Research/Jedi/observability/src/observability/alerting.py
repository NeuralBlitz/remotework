from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertState(str, Enum):
    FIRING = "firing"
    RESOLVED = "resolved"
    ACKNOWLEDGED = "acknowledged"


@dataclass
class Alert:
    id: str
    name: str
    severity: AlertSeverity
    message: str
    state: AlertState = AlertState.FIRING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: datetime | None = None
    labels: dict[str, str] = field(default_factory=dict)


class AlertManager:
    def __init__(self) -> None:
        self._alerts: dict[str, Alert] = {}
        self._rules: dict[str, dict[str, object]] = {}

    def fire(
        self,
        alert_id: str,
        name: str,
        severity: AlertSeverity,
        message: str,
        labels: dict[str, str] | None = None,
    ) -> Alert:
        if alert_id in self._alerts and self._alerts[alert_id].state == AlertState.FIRING:
            return self._alerts[alert_id]
        alert = Alert(
            id=alert_id, name=name, severity=severity, message=message, labels=labels or {}
        )
        self._alerts[alert_id] = alert
        return alert

    def resolve(self, alert_id: str) -> bool:
        alert = self._alerts.get(alert_id)
        if alert and alert.state == AlertState.FIRING:
            alert.state = AlertState.RESOLVED
            alert.resolved_at = datetime.now(timezone.utc)
            return True
        return False

    def acknowledge(self, alert_id: str) -> bool:
        alert = self._alerts.get(alert_id)
        if alert and alert.state == AlertState.FIRING:
            alert.state = AlertState.ACKNOWLEDGED
            return True
        return False

    def get_firing(self) -> list[Alert]:
        return [a for a in self._alerts.values() if a.state == AlertState.FIRING]

    def get_by_severity(self, severity: AlertSeverity) -> list[Alert]:
        return [a for a in self._alerts.values() if a.severity == severity]

    def add_rule(self, name: str, metric: str, threshold: float, severity: AlertSeverity) -> None:
        self._rules[name] = {"metric": metric, "threshold": threshold, "severity": severity}

    def remove_rule(self, name: str) -> bool:
        return self._rules.pop(name, None) is not None

    @property
    def alert_count(self) -> int:
        return len(self._alerts)

    @property
    def rule_count(self) -> int:
        return len(self._rules)
