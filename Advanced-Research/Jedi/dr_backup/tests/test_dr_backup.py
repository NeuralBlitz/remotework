import pytest
from datetime import datetime, timezone
from dr_backup.manager import BackupManager, BackupConfig, BackupType, BackupStatus
from dr_backup.scheduler import BackupScheduler, Schedule, ScheduleType
from dr_backup.storage import BackupStorage, BackupRecord


def test_backup_config_creation() -> None:
    cfg = BackupConfig(name="daily", database="mydb")
    assert cfg.name == "daily"
    assert cfg.backup_type == BackupType.FULL
    assert cfg.compress is True


def test_backup_config_validate() -> None:
    cfg = BackupConfig(name="", database="")
    errors = cfg.validate()
    assert "name is required" in errors
    assert "database is required" in errors


def test_backup_config_invalid_retention() -> None:
    cfg = BackupConfig(name="x", database="y", retention_days=0)
    errors = cfg.validate()
    assert "retention_days must be >= 1" in errors


def test_manager_add_config() -> None:
    mgr = BackupManager()
    mgr.add_config(BackupConfig(name="c1", database="db1"))
    assert mgr.config_count == 1


def test_manager_add_duplicate_raises() -> None:
    mgr = BackupManager()
    mgr.add_config(BackupConfig(name="c1", database="db1"))
    with pytest.raises(ValueError):
        mgr.add_config(BackupConfig(name="c1", database="db2"))


def test_manager_add_invalid_raises() -> None:
    mgr = BackupManager()
    with pytest.raises(ValueError):
        mgr.add_config(BackupConfig(name="", database="db"))


def test_manager_remove_config() -> None:
    mgr = BackupManager()
    mgr.add_config(BackupConfig(name="c1", database="db"))
    assert mgr.remove_config("c1")
    assert mgr.config_count == 0
    assert not mgr.remove_config("c1")


def test_manager_get_config_not_found() -> None:
    mgr = BackupManager()
    with pytest.raises(KeyError):
        mgr.get_config("nonexistent")


def test_manager_run_backup() -> None:
    mgr = BackupManager()
    mgr.add_config(BackupConfig(name="daily", database="prod"))
    record = mgr.run_backup("daily")
    assert record.status == BackupStatus.COMPLETED
    assert record.database == "prod"


def test_manager_history() -> None:
    mgr = BackupManager()
    mgr.add_config(BackupConfig(name="b1", database="db"))
    mgr.run_backup("b1")
    mgr.run_backup("b1")
    assert len(mgr.get_history("b1")) == 2
    assert len(mgr.get_history()) == 2


def test_schedule_creation() -> None:
    s = Schedule(name="s1", config_name="c1", schedule_type=ScheduleType.DAILY)
    assert s.enabled is True


def test_schedule_compute_next_run() -> None:
    s = Schedule(name="s1", config_name="c1", schedule_type=ScheduleType.HOURLY)
    base = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    nxt = s.compute_next_run(base)
    assert nxt.hour == 13


def test_scheduler_add_and_get() -> None:
    sched = BackupScheduler()
    s = Schedule(name="s1", config_name="c1", schedule_type=ScheduleType.DAILY)
    sched.add_schedule(s)
    assert sched.schedule_count == 1
    assert sched.get_schedule("s1").name == "s1"


def test_scheduler_add_duplicate_raises() -> None:
    sched = BackupScheduler()
    sched.add_schedule(Schedule(name="s1", config_name="c1", schedule_type=ScheduleType.DAILY))
    with pytest.raises(ValueError):
        sched.add_schedule(Schedule(name="s1", config_name="c2", schedule_type=ScheduleType.WEEKLY))


def test_scheduler_remove() -> None:
    sched = BackupScheduler()
    sched.add_schedule(Schedule(name="s1", config_name="c1", schedule_type=ScheduleType.DAILY))
    assert sched.remove_schedule("s1")
    assert sched.schedule_count == 0


def test_scheduler_enable_disable() -> None:
    sched = BackupScheduler()
    sched.add_schedule(Schedule(name="s1", config_name="c1", schedule_type=ScheduleType.DAILY))
    sched.disable_schedule("s1")
    assert not sched.get_schedule("s1").enabled
    sched.enable_schedule("s1")
    assert sched.get_schedule("s1").enabled


def test_scheduler_due_schedules() -> None:
    sched = BackupScheduler()
    sched.add_schedule(Schedule(name="s1", config_name="c1", schedule_type=ScheduleType.DAILY))
    due = sched.get_due_schedules()
    assert len(due) == 1


def test_storage_store_and_get() -> None:
    storage = BackupStorage()
    record = BackupRecord(
        config_name="c1",
        database="db1",
        backup_type=BackupType.FULL,
        status=BackupStatus.COMPLETED,
        started_at=datetime.now(timezone.utc),
    )
    storage.store(record)
    assert storage.record_count == 1
    assert len(storage.get_records("db1")) == 1


def test_storage_get_latest() -> None:
    storage = BackupStorage()
    now = datetime.now(timezone.utc)
    storage.store(BackupRecord("c1", "db1", BackupType.FULL, BackupStatus.COMPLETED, now))
    latest = storage.get_latest("db1")
    assert latest is not None
    assert latest.database == "db1"


def test_storage_get_latest_empty() -> None:
    storage = BackupStorage()
    assert storage.get_latest("db1") is None


def test_storage_get_records_all() -> None:
    storage = BackupStorage()
    now = datetime.now(timezone.utc)
    storage.store(BackupRecord("c1", "db1", BackupType.FULL, BackupStatus.COMPLETED, now))
    storage.store(BackupRecord("c2", "db2", BackupType.INCREMENTAL, BackupStatus.COMPLETED, now))
    assert len(storage.get_records()) == 2
