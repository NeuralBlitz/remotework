from pg_health.adapters import PgStatAdapter, ReplicationLagAdapter, SystemMetricAdapter
from pg_health.aggregator import HealthAggregator
from pg_health.models import HealthStatus, MetricPoint, SystemHealth


class TestMetricPoint:
    def test_defaults(self) -> None:
        mp = MetricPoint(name="cpu", value=50.0, unit="percent", source="os")
        assert mp.status == HealthStatus.HEALTHY

    def test_with_thresholds(self) -> None:
        mp = MetricPoint(
            name="lag",
            value=10.0,
            unit="seconds",
            source="repl",
            threshold_warning=5.0,
            threshold_critical=30.0,
        )
        assert mp.threshold_warning == 5.0


class TestSystemHealth:
    def test_is_healthy(self) -> None:
        metrics = [MetricPoint(name="x", value=1.0, unit="u", source="s")]
        sh = SystemHealth(overall_status=HealthStatus.HEALTHY, metrics=metrics)
        assert sh.is_healthy

    def test_not_healthy(self) -> None:
        sh = SystemHealth(overall_status=HealthStatus.CRITICAL, metrics=[])
        assert not sh.is_healthy

    def test_metrics_by_status(self) -> None:
        metrics = [
            MetricPoint(name="a", value=1.0, unit="u", source="s", status=HealthStatus.HEALTHY),
            MetricPoint(name="b", value=2.0, unit="u", source="s", status=HealthStatus.CRITICAL),
        ]
        sh = SystemHealth(overall_status=HealthStatus.CRITICAL, metrics=metrics)
        assert len(sh.metrics_by_status(HealthStatus.CRITICAL)) == 1

    def test_worst_status(self) -> None:
        metrics = [
            MetricPoint(name="a", value=1.0, unit="u", source="s", status=HealthStatus.HEALTHY),
            MetricPoint(name="b", value=2.0, unit="u", source="s", status=HealthStatus.DEGRADED),
        ]
        sh = SystemHealth(overall_status=HealthStatus.DEGRADED, metrics=metrics)
        assert sh.worst_status() == HealthStatus.DEGRADED


class TestPgStatAdapter:
    def test_healthy_connections(self) -> None:
        adapter = PgStatAdapter(active_connections=30, max_connections=100)
        metrics = adapter.collect()
        assert all(m.status == HealthStatus.HEALTHY for m in metrics)
        assert adapter.source_name == "pg_stat_activity"

    def test_degraded_connections(self) -> None:
        adapter = PgStatAdapter(active_connections=80, max_connections=100)
        metrics = adapter.collect()
        conn_metric = [m for m in metrics if m.name == "connection_usage_pct"][0]
        assert conn_metric.status == HealthStatus.DEGRADED

    def test_critical_connections(self) -> None:
        adapter = PgStatAdapter(active_connections=95, max_connections=100)
        metrics = adapter.collect()
        conn_metric = [m for m in metrics if m.name == "connection_usage_pct"][0]
        assert conn_metric.status == HealthStatus.CRITICAL

    def test_waiting_connections(self) -> None:
        adapter = PgStatAdapter(waiting_connections=5)
        metrics = adapter.collect()
        wait = [m for m in metrics if m.name == "waiting_connections"][0]
        assert wait.status == HealthStatus.CRITICAL


class TestReplicationLagAdapter:
    def test_healthy_lag(self) -> None:
        adapter = ReplicationLagAdapter(lag_seconds=0.5, lag_bytes=1024)
        metrics = adapter.collect()
        assert all(m.status == HealthStatus.HEALTHY for m in metrics)

    def test_degraded_lag(self) -> None:
        adapter = ReplicationLagAdapter(lag_seconds=10)
        metrics = adapter.collect()
        lag = [m for m in metrics if m.name == "replication_lag_seconds"][0]
        assert lag.status == HealthStatus.DEGRADED

    def test_critical_lag(self) -> None:
        adapter = ReplicationLagAdapter(lag_seconds=60)
        metrics = adapter.collect()
        lag = [m for m in metrics if m.name == "replication_lag_seconds"][0]
        assert lag.status == HealthStatus.CRITICAL


class TestSystemMetricAdapter:
    def test_healthy_system(self) -> None:
        adapter = SystemMetricAdapter(cpu_percent=20, memory_percent=40, disk_usage_percent=30)
        metrics = adapter.collect()
        assert all(m.status == HealthStatus.HEALTHY for m in metrics)

    def test_critical_cpu(self) -> None:
        adapter = SystemMetricAdapter(cpu_percent=95)
        metrics = adapter.collect()
        cpu = [m for m in metrics if m.name == "cpu_percent"][0]
        assert cpu.status == HealthStatus.CRITICAL


class TestHealthAggregator:
    def test_register_and_collect(self) -> None:
        agg = HealthAggregator()
        agg.register_adapter(PgStatAdapter(active_connections=50, max_connections=100))
        agg.register_adapter(SystemMetricAdapter(cpu_percent=30))
        assert agg.adapter_count == 2
        health = agg.collect_all()
        assert health.overall_status == HealthStatus.HEALTHY
        assert len(health.sources) == 2

    def test_critical_propagation(self) -> None:
        agg = HealthAggregator()
        agg.register_adapter(PgStatAdapter(active_connections=95, max_connections=100))
        agg.register_adapter(SystemMetricAdapter(cpu_percent=95))
        health = agg.collect_all()
        assert health.overall_status == HealthStatus.CRITICAL
        crits = agg.get_critical_metrics(health)
        assert len(crits) > 0

    def test_no_adapters(self) -> None:
        agg = HealthAggregator()
        health = agg.collect_all()
        assert health.overall_status == HealthStatus.UNKNOWN
