import pytest
from datetime import datetime, timezone
from observability.metrics import MetricsCollector, Metric, MetricType
from observability.tracing import Tracer, Span
from observability.alerting import AlertManager, Alert, AlertSeverity, AlertState


def test_metric_creation() -> None:
    m = Metric(name="requests", metric_type=MetricType.COUNTER)
    assert m.value == 0.0


def test_collector_register() -> None:
    c = MetricsCollector()
    m = c.register("http_requests", MetricType.COUNTER, "Total requests")
    assert m.name == "http_requests"
    assert c.metric_count == 1


def test_collector_register_duplicate_raises() -> None:
    c = MetricsCollector()
    c.register("m1", MetricType.COUNTER)
    with pytest.raises(ValueError):
        c.register("m1", MetricType.GAUGE)


def test_collector_increment() -> None:
    c = MetricsCollector()
    c.register("c", MetricType.COUNTER)
    c.increment("c")
    c.increment("c", 5.0)
    assert c.get("c").value == 6.0


def test_collector_set_gauge() -> None:
    c = MetricsCollector()
    c.register("g", MetricType.GAUGE)
    c.set_gauge("g", 42.0)
    assert c.get("g").value == 42.0


def test_collector_observe() -> None:
    c = MetricsCollector()
    c.register("h", MetricType.HISTOGRAM)
    c.observe("h", 0.123)
    assert c.get("h").value == 0.123


def test_collector_reset() -> None:
    c = MetricsCollector()
    c.register("m", MetricType.COUNTER)
    c.increment("m", 10)
    c.reset("m")
    assert c.get("m").value == 0.0


def test_collector_get_not_found() -> None:
    c = MetricsCollector()
    with pytest.raises(KeyError):
        c.get("missing")


def test_collector_get_all() -> None:
    c = MetricsCollector()
    c.register("a", MetricType.COUNTER)
    c.register("b", MetricType.GAUGE)
    assert len(c.get_all()) == 2


def test_span_creation() -> None:
    s = Span(trace_id="t1", span_id="s1", operation="query")
    assert s.duration_ms is None


def test_span_finish() -> None:
    s = Span(trace_id="t1", span_id="s1", operation="query")
    s.finish()
    assert s.end_time is not None
    assert s.duration_ms is not None


def test_span_set_tag() -> None:
    s = Span(trace_id="t1", span_id="s1", operation="q")
    s.set_tag("db", "postgres")
    assert s.tags["db"] == "postgres"


def test_span_log() -> None:
    s = Span(trace_id="t1", span_id="s1", operation="q")
    s.log("executing", rows=10)
    assert len(s.logs) == 1


def test_tracer_start_trace() -> None:
    t = Tracer()
    s = t.start_trace("main")
    assert s.trace_id == "trace-1"
    assert s.span_id == "span-1"
    assert t.span_count == 1


def test_tracer_child_span() -> None:
    t = Tracer()
    parent = t.start_trace("parent")
    child = t.start_child_span(parent, "child")
    assert child.trace_id == parent.trace_id
    assert child.parent_id == parent.span_id


def test_tracer_get_spans_for_trace() -> None:
    t = Tracer()
    s = t.start_trace("op")
    t.start_child_span(s, "child")
    assert len(t.get_spans_for_trace(s.trace_id)) == 2


def test_tracer_error_spans() -> None:
    t = Tracer()
    s = t.start_trace("op")
    s.error = "timeout"
    assert len(t.get_error_spans()) == 1


def test_alert_fire() -> None:
    mgr = AlertManager()
    a = mgr.fire("a1", "high_cpu", AlertSeverity.WARNING, "CPU > 90%")
    assert a.state == AlertState.FIRING
    assert mgr.alert_count == 1


def test_alert_fire_idempotent() -> None:
    mgr = AlertManager()
    mgr.fire("a1", "high_cpu", AlertSeverity.WARNING, "msg")
    mgr.fire("a1", "high_cpu", AlertSeverity.CRITICAL, "msg2")
    assert mgr.alert_count == 1


def test_alert_resolve() -> None:
    mgr = AlertManager()
    mgr.fire("a1", "cpu", AlertSeverity.WARNING, "msg")
    assert mgr.resolve("a1")
    assert mgr.get_firing() == []


def test_alert_acknowledge() -> None:
    mgr = AlertManager()
    mgr.fire("a1", "cpu", AlertSeverity.WARNING, "msg")
    assert mgr.acknowledge("a1")
    assert mgr.get_firing() == []


def test_alert_resolve_not_firing() -> None:
    mgr = AlertManager()
    assert not mgr.resolve("nonexistent")


def test_alert_get_by_severity() -> None:
    mgr = AlertManager()
    mgr.fire("a1", "n", AlertSeverity.CRITICAL, "m")
    mgr.fire("a2", "n", AlertSeverity.WARNING, "m")
    assert len(mgr.get_by_severity(AlertSeverity.CRITICAL)) == 1


def test_alert_rules() -> None:
    mgr = AlertManager()
    mgr.add_rule("cpu_high", "cpu_usage", 90.0, AlertSeverity.CRITICAL)
    assert mgr.rule_count == 1
    assert mgr.remove_rule("cpu_high")
    assert mgr.rule_count == 0


def test_alert_remove_missing_rule() -> None:
    mgr = AlertManager()
    assert not mgr.remove_rule("nope")
