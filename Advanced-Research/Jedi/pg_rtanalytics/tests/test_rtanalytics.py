"""Tests for pg_rtanalytics."""

from __future__ import annotations

from pg_rtanalytics.models import EventType, NotificationEvent, ThresholdConfig
from pg_rtanalytics.observers import DashboardObserver, WebhookObserver
from pg_rtanalytics.subject import TableUpdateSubject


class TestThresholdConfig:
    def test_default_values(self) -> None:
        config = ThresholdConfig()
        assert config.min_amount == 1000.0
        assert config.max_amount == 1_000_000.0
        assert "transactions" in config.watched_tables

    def test_is_above_threshold(self) -> None:
        config = ThresholdConfig(min_amount=500.0)
        assert config.is_above_threshold(600.0)
        assert not config.is_above_threshold(400.0)
        assert not config.is_above_threshold(500.0)

    def test_is_watched_table(self) -> None:
        config = ThresholdConfig(watched_tables=["orders"])
        assert config.is_watched_table("orders")
        assert not config.is_watched_table("users")


class TestNotificationEvent:
    def test_creation(self) -> None:
        event = NotificationEvent(
            table_name="orders",
            event_type=EventType.INSERT,
            row_data={"id": 1, "amount": 500.0},
        )
        assert event.table_name == "orders"
        assert event.event_type == EventType.INSERT

    def test_is_high_value(self) -> None:
        event = NotificationEvent(
            table_name="orders",
            event_type=EventType.INSERT,
            row_data={"amount": 2000.0},
            threshold=1000.0,
        )
        assert event.is_high_value

    def test_not_high_value(self) -> None:
        event = NotificationEvent(
            table_name="orders",
            event_type=EventType.INSERT,
            row_data={"amount": 500.0},
            threshold=1000.0,
        )
        assert not event.is_high_value


class TestTableUpdateSubject:
    def test_attach_detach(self) -> None:
        subject = TableUpdateSubject()
        observer = WebhookObserver(webhook_url="http://example.com")
        subject.attach(observer)
        assert subject.observer_count == 1
        subject.detach(observer)
        assert subject.observer_count == 0

    def test_no_duplicate_attach(self) -> None:
        subject = TableUpdateSubject()
        observer = WebhookObserver(webhook_url="http://example.com")
        subject.attach(observer)
        subject.attach(observer)
        assert subject.observer_count == 1

    def test_notify(self) -> None:
        subject = TableUpdateSubject()
        wh = WebhookObserver(webhook_url="http://example.com")
        dash = DashboardObserver(dashboard_id="d1")
        subject.attach(wh)
        subject.attach(dash)
        event = NotificationEvent(
            table_name="transactions",
            event_type=EventType.INSERT,
            row_data={"amount": 2000.0},
        )
        subject.notify(event)
        assert len(wh.received_events) == 1
        assert dash.metrics["total"] == 1

    def test_process_insert_watched_table(self) -> None:
        config = ThresholdConfig(watched_tables=["orders"], min_amount=100.0)
        subject = TableUpdateSubject(config=config)
        wh = WebhookObserver(webhook_url="http://example.com")
        subject.attach(wh)
        result = subject.process_insert("orders", {"id": 1, "amount": 500.0})
        assert result is not None
        assert subject.event_count == 1
        assert len(wh.received_events) == 1

    def test_process_insert_unwatched_table(self) -> None:
        config = ThresholdConfig(watched_tables=["orders"])
        subject = TableUpdateSubject(config=config)
        result = subject.process_insert("users", {"id": 1, "amount": 5000.0})
        assert result is None

    def test_process_insert_below_threshold(self) -> None:
        config = ThresholdConfig(watched_tables=["orders"], min_amount=1000.0)
        subject = TableUpdateSubject(config=config)
        wh = WebhookObserver(webhook_url="http://example.com")
        subject.attach(wh)
        result = subject.process_insert("orders", {"id": 1, "amount": 500.0})
        assert result is not None
        assert len(wh.received_events) == 0


class TestWebhookObserver:
    def test_receives_events(self) -> None:
        wh = WebhookObserver(webhook_url="http://example.com/hook")
        event = NotificationEvent(
            table_name="orders",
            event_type=EventType.INSERT,
            row_data={"amount": 2000.0},
        )
        wh.on_notify(event)
        assert len(wh.received_events) == 1

    def test_error_tracking(self) -> None:
        wh = WebhookObserver(webhook_url="http://example.com/hook")
        wh.on_error(ValueError("test"))
        assert wh.error_count == 1


class TestDashboardObserver:
    def test_metrics_aggregation(self) -> None:
        dash = DashboardObserver(dashboard_id="d1")
        for _ in range(3):
            event = NotificationEvent(
                table_name="orders",
                event_type=EventType.INSERT,
                row_data={"amount": 2000.0},
            )
            dash.on_notify(event)
        assert dash.metrics["total"] == 3
        assert dash.metrics["by_table"]["orders"] == 3

    def test_multi_table_metrics(self) -> None:
        dash = DashboardObserver(dashboard_id="d1")
        dash.on_notify(
            NotificationEvent(
                table_name="orders", event_type=EventType.INSERT, row_data={"amount": 100.0}
            )
        )
        dash.on_notify(
            NotificationEvent(
                table_name="transactions", event_type=EventType.INSERT, row_data={"amount": 200.0}
            )
        )
        assert dash.metrics["by_table"]["orders"] == 1
        assert dash.metrics["by_table"]["transactions"] == 1

    def test_reset(self) -> None:
        dash = DashboardObserver(dashboard_id="d1")
        dash.on_notify(
            NotificationEvent(
                table_name="orders", event_type=EventType.INSERT, row_data={"amount": 100.0}
            )
        )
        dash.reset()
        assert dash.metrics["total"] == 0
