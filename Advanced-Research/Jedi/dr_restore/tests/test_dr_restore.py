import pytest
from datetime import datetime, timezone
from dr_restore.engine import RestoreEngine, RestoreConfig, RestoreMode, RestoreStatus
from dr_restore.validator import RestoreValidator, ValidationStatus, ValidationResult
from dr_restore.recovery import RecoveryManager, RecoveryPoint, RecoveryType


def test_restore_config_creation() -> None:
    cfg = RestoreConfig(name="r1", source_backup="b1", target_database="db1")
    assert cfg.mode == RestoreMode.FULL
    assert cfg.overwrite is False


def test_restore_config_validate() -> None:
    cfg = RestoreConfig(name="", source_backup="", target_database="")
    errors = cfg.validate()
    assert "name is required" in errors
    assert "source_backup is required" in errors
    assert "target_database is required" in errors


def test_restore_config_pit_requires_time() -> None:
    cfg = RestoreConfig(
        name="r1", source_backup="b1", target_database="db1", mode=RestoreMode.POINT_IN_TIME
    )
    errors = cfg.validate()
    assert "point_in_time is required for point_in_time mode" in errors


def test_restore_config_selective_requires_tables() -> None:
    cfg = RestoreConfig(
        name="r1", source_backup="b1", target_database="db1", mode=RestoreMode.SELECTIVE
    )
    errors = cfg.validate()
    assert "target_tables required for selective mode" in errors


def test_engine_add_config() -> None:
    eng = RestoreEngine()
    eng.add_config(RestoreConfig(name="r1", source_backup="b1", target_database="db1"))
    assert eng.config_count == 1


def test_engine_add_duplicate_raises() -> None:
    eng = RestoreEngine()
    eng.add_config(RestoreConfig(name="r1", source_backup="b1", target_database="db1"))
    with pytest.raises(ValueError):
        eng.add_config(RestoreConfig(name="r1", source_backup="b2", target_database="db2"))


def test_engine_add_invalid_raises() -> None:
    eng = RestoreEngine()
    with pytest.raises(ValueError):
        eng.add_config(RestoreConfig(name="", source_backup="b1", target_database="db1"))


def test_engine_remove_config() -> None:
    eng = RestoreEngine()
    eng.add_config(RestoreConfig(name="r1", source_backup="b1", target_database="db1"))
    assert eng.remove_config("r1")
    assert eng.config_count == 0


def test_engine_get_config_not_found() -> None:
    eng = RestoreEngine()
    with pytest.raises(KeyError):
        eng.get_config("nope")


def test_engine_run_restore() -> None:
    eng = RestoreEngine()
    eng.add_config(RestoreConfig(name="r1", source_backup="b1", target_database="db1"))
    result = eng.run_restore("r1")
    assert result["status"] == RestoreStatus.COMPLETED.value


def test_engine_history() -> None:
    eng = RestoreEngine()
    eng.add_config(RestoreConfig(name="r1", source_backup="b1", target_database="db1"))
    eng.run_restore("r1")
    assert len(eng.get_history()) == 1


def test_validator_backup_exists() -> None:
    v = RestoreValidator()
    result = v.validate_backup_exists("backup1")
    assert result.is_valid
    assert v.checks_run == 1


def test_validator_backup_empty() -> None:
    v = RestoreValidator()
    result = v.validate_backup_exists("")
    assert not result.is_valid


def test_validator_target_available() -> None:
    v = RestoreValidator()
    assert v.validate_target_available("db1").is_valid
    assert not v.validate_target_available("").is_valid


def test_validator_disk_space_ok() -> None:
    v = RestoreValidator()
    result = v.validate_disk_space(10.0, 20.0)
    assert result.status == ValidationStatus.VALID


def test_validator_disk_space_low() -> None:
    v = RestoreValidator()
    result = v.validate_disk_space(10.0, 12.0)
    assert result.status == ValidationStatus.WARNING


def test_validator_disk_space_insufficient() -> None:
    v = RestoreValidator()
    result = v.validate_disk_space(10.0, 5.0)
    assert not result.is_valid


def test_validator_version_match() -> None:
    v = RestoreValidator()
    assert v.validate_version_compatibility("16.1", "16.2").is_valid


def test_validator_version_mismatch() -> None:
    v = RestoreValidator()
    result = v.validate_version_compatibility("15.0", "16.0")
    assert not result.is_valid


def test_recovery_add_point() -> None:
    mgr = RecoveryManager()
    pt = RecoveryPoint(
        id="p1",
        timestamp=datetime.now(timezone.utc),
        recovery_type=RecoveryType.FULL,
        source_backup="b1",
    )
    mgr.add_recovery_point(pt)
    assert mgr.recovery_point_count == 1


def test_recovery_add_duplicate_raises() -> None:
    mgr = RecoveryManager()
    pt = RecoveryPoint(
        id="p1",
        timestamp=datetime.now(timezone.utc),
        recovery_type=RecoveryType.FULL,
        source_backup="b1",
    )
    mgr.add_recovery_point(pt)
    with pytest.raises(ValueError):
        mgr.add_recovery_point(pt)


def test_recovery_get_not_found() -> None:
    mgr = RecoveryManager()
    with pytest.raises(KeyError):
        mgr.get_recovery_point("nope")


def test_recovery_list_and_filter() -> None:
    mgr = RecoveryManager()
    now = datetime.now(timezone.utc)
    mgr.add_recovery_point(RecoveryPoint("p1", now, RecoveryType.FULL, "b1"))
    mgr.add_recovery_point(RecoveryPoint("p2", now, RecoveryType.INCREMENTAL, "b2"))
    assert len(mgr.list_recovery_points()) == 2
    assert len(mgr.list_recovery_points("b1")) == 1


def test_recovery_verify() -> None:
    mgr = RecoveryManager()
    mgr.add_recovery_point(RecoveryPoint("p1", datetime.now(timezone.utc), RecoveryType.FULL, "b1"))
    assert mgr.verify_recovery_point("p1")
    assert mgr.get_recovery_point("p1").verified


def test_recovery_latest() -> None:
    mgr = RecoveryManager()
    t1 = datetime(2024, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2024, 6, 1, tzinfo=timezone.utc)
    mgr.add_recovery_point(RecoveryPoint("p1", t1, RecoveryType.FULL, "b1"))
    mgr.add_recovery_point(RecoveryPoint("p2", t2, RecoveryType.FULL, "b1"))
    latest = mgr.get_latest_recovery_point()
    assert latest is not None
    assert latest.id == "p2"


def test_recovery_latest_empty() -> None:
    mgr = RecoveryManager()
    assert mgr.get_latest_recovery_point() is None


def test_recovery_recover() -> None:
    mgr = RecoveryManager()
    mgr.add_recovery_point(RecoveryPoint("p1", datetime.now(timezone.utc), RecoveryType.FULL, "b1"))
    result = mgr.recover("p1")
    assert result["status"] == "completed"
    assert mgr.operation_count == 1
