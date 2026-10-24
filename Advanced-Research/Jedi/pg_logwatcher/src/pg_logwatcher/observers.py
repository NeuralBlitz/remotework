from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pg_logwatcher.models import LogEntry

from pg_logwatcher.models import AlertEvent, LogLevel


class SlowQueryObserver:
    def __init__(self, threshold_ms: float = 1000.0) -> None:
        self.threshold_ms = threshold_ms
        self.alerts: list[AlertEvent] = []

    def on_log_entry(self, entry: LogEntry) -> None:
        if entry.duration_ms is not None and entry.duration_ms > self.threshold_ms:
            alert = AlertEvent(
                alert_id=str(uuid.uuid4()),
                source_entry=entry,
                alert_type="slow_query",
                description=f"Query took {entry.duration_ms}ms (threshold: {self.threshold_ms}ms)",
                severity=LogLevel.WARNING,
            )
            self.alerts.append(alert)


class FatalErrorObserver:
    def __init__(self) -> None:
        self.alerts: list[AlertEvent] = []

    def on_log_entry(self, entry: LogEntry) -> None:
        if entry.level in (LogLevel.FATAL, LogLevel.PANIC):
            alert = AlertEvent(
                alert_id=str(uuid.uuid4()),
                source_entry=entry,
                alert_type="fatal_error",
                description=f"Fatal error detected: {entry.message}",
                severity=LogLevel.FATAL,
            )
            self.alerts.append(alert)


class AlertManager:
    def __init__(self) -> None:
        self.alerts: list[AlertEvent] = []

    def on_log_entry(self, entry: LogEntry) -> None:
        pass

    def collect_alerts(
        self, *observers: SlowQueryObserver | FatalErrorObserver
    ) -> list[AlertEvent]:
        all_alerts: list[AlertEvent] = []
        for obs in observers:
            all_alerts.extend(obs.alerts)
        all_alerts.sort(key=lambda a: a.created_at)
        self.alerts = all_alerts
        return all_alerts

    def alerts_by_type(self, alert_type: str) -> list[AlertEvent]:
        return [a for a in self.alerts if a.alert_type == alert_type]
