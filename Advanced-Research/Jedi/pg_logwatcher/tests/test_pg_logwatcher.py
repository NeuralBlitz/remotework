from datetime import datetime

from pg_logwatcher.models import LogEntry, LogLevel
from pg_logwatcher.observers import AlertManager, FatalErrorObserver, SlowQueryObserver
from pg_logwatcher.subject import LogStream


def _make_entry(
    level: LogLevel = LogLevel.INFO,
    message: str = "test",
    duration_ms: float | None = None,
    query: str | None = None,
) -> LogEntry:
    return LogEntry(
        timestamp=datetime.now(),
        level=level,
        message=message,
        duration_ms=duration_ms,
        query=query,
    )


class TestLogLevel:
    def test_enum_values(self) -> None:
        assert LogLevel.FATAL.value == "FATAL"
        assert LogLevel.DEBUG.value == "DEBUG"

    def test_log_entry_immutable(self) -> None:
        entry = _make_entry()
        try:
            entry.message = "changed"  # type: ignore[misc]
        except AttributeError:
            pass
        assert entry.message == "test"


class TestLogStream:
    def test_subscribe_and_emit(self) -> None:
        stream = LogStream()
        observer = FatalErrorObserver()
        stream.subscribe(observer)
        assert stream.observer_count == 1
        entry = _make_entry(level=LogLevel.FATAL, message="crash")
        stream.emit(entry)
        assert len(observer.alerts) == 1
        assert len(stream.entries) == 1

    def test_unsubscribe(self) -> None:
        stream = LogStream()
        observer = FatalErrorObserver()
        stream.subscribe(observer)
        stream.unsubscribe(observer)
        assert stream.observer_count == 0

    def test_multiple_observers(self) -> None:
        stream = LogStream()
        obs1 = FatalErrorObserver()
        obs2 = SlowQueryObserver()
        stream.subscribe(obs1)
        stream.subscribe(obs2)
        stream.emit(_make_entry(level=LogLevel.FATAL, message="bad", duration_ms=5000))
        assert len(obs1.alerts) == 1
        assert len(obs2.alerts) == 1


class TestSlowQueryObserver:
    def test_slow_query_triggers_alert(self) -> None:
        observer = SlowQueryObserver(threshold_ms=500.0)
        entry = _make_entry(duration_ms=1200.0, query="SELECT * FROM big_table")
        observer.on_log_entry(entry)
        assert len(observer.alerts) == 1
        assert observer.alerts[0].alert_type == "slow_query"

    def test_fast_query_no_alert(self) -> None:
        observer = SlowQueryObserver(threshold_ms=500.0)
        entry = _make_entry(duration_ms=100.0)
        observer.on_log_entry(entry)
        assert len(observer.alerts) == 0

    def test_no_duration_no_alert(self) -> None:
        observer = SlowQueryObserver()
        entry = _make_entry(duration_ms=None)
        observer.on_log_entry(entry)
        assert len(observer.alerts) == 0


class TestFatalErrorObserver:
    def test_fatal_triggers_alert(self) -> None:
        observer = FatalErrorObserver()
        observer.on_log_entry(_make_entry(LogLevel.FATAL, "database system is shutting down"))
        assert len(observer.alerts) == 1
        assert observer.alerts[0].severity == LogLevel.FATAL

    def test_panic_triggers_alert(self) -> None:
        observer = FatalErrorObserver()
        observer.on_log_entry(_make_entry(LogLevel.PANIC, "unrecoverable"))
        assert len(observer.alerts) == 1

    def test_info_no_alert(self) -> None:
        observer = FatalErrorObserver()
        observer.on_log_entry(_make_entry(LogLevel.INFO, "all good"))
        assert len(observer.alerts) == 0


class TestAlertManager:
    def test_collect_alerts(self) -> None:
        slow = SlowQueryObserver(threshold_ms=100)
        fatal = FatalErrorObserver()
        manager = AlertManager()
        slow.on_log_entry(_make_entry(duration_ms=500))
        fatal.on_log_entry(_make_entry(LogLevel.FATAL, "down"))
        alerts = manager.collect_alerts(slow, fatal)
        assert len(alerts) == 2

    def test_alerts_by_type(self) -> None:
        slow = SlowQueryObserver(threshold_ms=100)
        fatal = FatalErrorObserver()
        manager = AlertManager()
        slow.on_log_entry(_make_entry(duration_ms=500))
        fatal.on_log_entry(_make_entry(LogLevel.FATAL, "down"))
        manager.collect_alerts(slow, fatal)
        assert len(manager.alerts_by_type("slow_query")) == 1
        assert len(manager.alerts_by_type("fatal_error")) == 1

    def test_duplicate_subscribe_no_duplicate_notify(self) -> None:
        stream = LogStream()
        observer = FatalErrorObserver()
        stream.subscribe(observer)
        stream.subscribe(observer)
        stream.emit(_make_entry(LogLevel.FATAL, "oops"))
        assert len(observer.alerts) == 1
