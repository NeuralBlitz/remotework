"""Concrete observer implementations."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from pg_rtanalytics.models import NotificationEvent

logger = logging.getLogger(__name__)


@dataclass
class WebhookObserver:
    """Sends notifications to a webhook URL."""

    webhook_url: str
    name: str = "webhook"
    received_events: list[NotificationEvent] = field(default_factory=list)
    _errors: list[Exception] = field(default_factory=list)

    def on_notify(self, event: NotificationEvent) -> None:
        self.received_events.append(event)
        logger.info("Webhook %s received event for %s", self.webhook_url, event.table_name)

    def on_error(self, error: Exception) -> None:
        self._errors.append(error)

    @property
    def error_count(self) -> int:
        return len(self._errors)


@dataclass
class DashboardObserver:
    """Aggregates events for a real-time dashboard."""

    dashboard_id: str
    name: str = "dashboard"
    metrics: dict[str, Any] = field(default_factory=lambda: {"total": 0, "by_table": {}})

    def on_notify(self, event: NotificationEvent) -> None:
        self.metrics["total"] += 1
        table = event.table_name
        by_table: dict[str, int] = self.metrics["by_table"]
        by_table[table] = by_table.get(table, 0) + 1

    def on_error(self, error: Exception) -> None:
        logger.error("Dashboard %s error: %s", self.dashboard_id, error)

    def reset(self) -> None:
        self.metrics = {"total": 0, "by_table": {}}
