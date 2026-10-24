import pytest

from pg_selfhealer.models import HealthStatus, IndexHealth, RebuildJob
from pg_selfhealer.observers import CorruptionObserver, RebuildObserver
from pg_selfhealer.subject import IndexHealthMonitor


def _make_health(
    name: str = "idx_users", status: HealthStatus = HealthStatus.HEALTHY, **kw: object
) -> IndexHealth:
    return IndexHealth(index_name=name, table_name="users", status=status, **kw)


class TestIndexHealth:
    def test_healthy_not_needs_rebuild(self) -> None:
        h = _make_health()
        assert h.needs_rebuild is False

    def test_corrupt_needs_rebuild(self) -> None:
        h = _make_health(status=HealthStatus.CORRUPT)
        assert h.needs_rebuild is True

    def test_high_bloat_needs_rebuild(self) -> None:
        h = _make_health(bloat_pct=50.0)
        assert h.needs_rebuild is True


class TestRebuildJob:
    def test_start(self) -> None:
        job = RebuildJob(index_name="idx1", table_name="t1")
        job.start()
        assert job.status == "running"
        assert job.started_at is not None

    def test_complete(self) -> None:
        job = RebuildJob(index_name="idx1", table_name="t1")
        job.start()
        job.complete()
        assert job.status == "completed"
        assert job.completed_at is not None

    def test_fail(self) -> None:
        job = RebuildJob(index_name="idx1", table_name="t1")
        job.start()
        job.fail("disk full")
        assert job.status == "failed"
        assert job.error == "disk full"


class TestIndexHealthMonitor:
    def test_register_and_check(self) -> None:
        monitor = IndexHealthMonitor()
        monitor.register_index(_make_health())
        health = monitor.check_health("idx_users")
        assert health.status == HealthStatus.HEALTHY

    def test_check_unknown_raises(self) -> None:
        monitor = IndexHealthMonitor()
        with pytest.raises(KeyError):
            monitor.check_health("missing")

    def test_corruption_notifies_observers(self) -> None:
        monitor = IndexHealthMonitor()
        corr = CorruptionObserver()
        monitor.attach(corr)
        monitor.register_index(_make_health(status=HealthStatus.CORRUPT))
        monitor.check_health("idx_users")
        assert len(corr.corruptions) == 1

    def test_rebuild_observer_triggers_on_needs_rebuild(self) -> None:
        monitor = IndexHealthMonitor()
        reb = RebuildObserver()
        monitor.attach(reb)
        monitor.register_index(_make_health(bloat_pct=50.0))
        monitor.check_health("idx_users")
        assert "idx_users" in reb.rebuilds_triggered

    def test_trigger_rebuild(self) -> None:
        monitor = IndexHealthMonitor()
        monitor.register_index(_make_health(status=HealthStatus.CORRUPT))
        job = monitor.trigger_rebuild("idx_users")
        assert job.status == "running"
        assert len(monitor.jobs) == 1

    def test_complete_rebuild_restores_health(self) -> None:
        monitor = IndexHealthMonitor()
        monitor.register_index(_make_health(status=HealthStatus.CORRUPT))
        job = monitor.trigger_rebuild("idx_users")
        monitor.complete_rebuild(job)
        assert monitor.indexes["idx_users"].status == HealthStatus.HEALTHY

    def test_detach_observer(self) -> None:
        monitor = IndexHealthMonitor()
        corr = CorruptionObserver()
        monitor.attach(corr)
        monitor.detach(corr)
        monitor.register_index(_make_health(status=HealthStatus.CORRUPT))
        monitor.check_health("idx_users")
        assert len(corr.corruptions) == 0

    def test_check_all(self) -> None:
        monitor = IndexHealthMonitor()
        monitor.register_index(_make_health(name="idx1"))
        monitor.register_index(_make_health(name="idx2"))
        results = monitor.check_all()
        assert len(results) == 2
