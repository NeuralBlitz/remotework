from datetime import datetime, timedelta

from pg_patchscheduler.mediator import PatchMediator
from pg_patchscheduler.models import CloudProvider, PatchStatus, PatchWindow
from pg_patchscheduler.scheduler import PatchScheduler


def _make_window(
    provider: CloudProvider = CloudProvider.AWS_RDS,
    instance: str = "db-1",
    start_hours: int = 0,
    duration_minutes: int = 30,
    version: str = "15.2",
    priority: int = 5,
) -> PatchWindow:
    return PatchWindow(
        provider=provider,
        instance_id=instance,
        start_time=datetime(2026, 3, 23, start_hours, 0),
        duration=timedelta(minutes=duration_minutes),
        patch_version=version,
        priority=priority,
    )


class TestPatchWindow:
    def test_end_time(self) -> None:
        w = _make_window(start_hours=10, duration_minutes=30)
        assert w.end_time == datetime(2026, 3, 23, 10, 30)

    def test_overlaps_true(self) -> None:
        a = _make_window(start_hours=10, duration_minutes=60)
        b = _make_window(start_hours=10, duration_minutes=30)
        assert a.overlaps(b)

    def test_overlaps_false(self) -> None:
        a = _make_window(start_hours=8, duration_minutes=60)
        b = _make_window(start_hours=10, duration_minutes=30)
        assert not a.overlaps(b)

    def test_no_overlap_adjacent(self) -> None:
        a = _make_window(start_hours=8, duration_minutes=60)
        b = _make_window(start_hours=9, duration_minutes=30)
        assert not a.overlaps(b)


class TestPatchMediator:
    def test_register_window(self) -> None:
        mediator = PatchMediator()
        mediator.register_window(_make_window())
        assert mediator.window_count == 1

    def test_resolve_no_conflicts(self) -> None:
        mediator = PatchMediator(min_gap=timedelta(minutes=0))
        w1 = _make_window(start_hours=8, duration_minutes=30)
        w2 = _make_window(start_hours=10, duration_minutes=30)
        mediator.register_window(w1)
        mediator.register_window(w2)
        resolved = mediator.resolve_conflicts()
        assert len(resolved) == 2
        assert all(w.status == PatchStatus.SCHEDULED for w in resolved)

    def test_resolve_conflicts_shifts(self) -> None:
        mediator = PatchMediator(min_gap=timedelta(hours=1))
        w1 = _make_window(instance="db-1", start_hours=10, duration_minutes=30)
        w2 = _make_window(instance="db-2", start_hours=10, duration_minutes=30)
        mediator.register_window(w1)
        mediator.register_window(w2)
        resolved = mediator.resolve_conflicts()
        assert resolved[0].start_time == datetime(2026, 3, 23, 10, 0)
        assert resolved[1].start_time > resolved[0].end_time

    def test_get_windows_by_provider(self) -> None:
        mediator = PatchMediator()
        mediator.register_window(_make_window(provider=CloudProvider.AWS_RDS))
        mediator.register_window(_make_window(provider=CloudProvider.AZURE))
        mediator.resolve_conflicts()
        aws = mediator.get_windows_by_provider("aws_rds")
        assert len(aws) == 1


class TestPatchScheduler:
    def test_add_and_schedule(self) -> None:
        scheduler = PatchScheduler()
        scheduler.add_window(_make_window(start_hours=8))
        scheduler.add_window(_make_window(start_hours=12))
        scheduled = scheduler.schedule_all()
        assert len(scheduled) == 2

    def test_execute_patch(self) -> None:
        scheduler = PatchScheduler()
        window = _make_window()
        scheduler.add_window(window)
        scheduler.schedule_all()
        result = scheduler.execute_patch(window)
        assert result.success
        assert result.new_version == "15.2"
        assert window.status == PatchStatus.COMPLETED

    def test_execute_all(self) -> None:
        scheduler = PatchScheduler()
        scheduler.add_window(_make_window(instance="db-1", start_hours=8))
        scheduler.add_window(_make_window(instance="db-2", start_hours=12))
        results = scheduler.execute_all()
        assert len(results) == 2
        assert all(r.success for r in results)

    def test_results_history(self) -> None:
        scheduler = PatchScheduler()
        scheduler.add_window(_make_window())
        scheduler.execute_all()
        assert len(scheduler.results) == 1

    def test_conflict_resolution_with_execute_all(self) -> None:
        scheduler = PatchScheduler(mediator=PatchMediator(min_gap=timedelta(hours=1)))
        scheduler.add_window(_make_window(instance="a", start_hours=10, duration_minutes=60))
        scheduler.add_window(_make_window(instance="b", start_hours=10, duration_minutes=60))
        results = scheduler.execute_all()
        assert len(results) == 2
        windows = [r.window for r in results]
        assert windows[0].start_time < windows[1].start_time
