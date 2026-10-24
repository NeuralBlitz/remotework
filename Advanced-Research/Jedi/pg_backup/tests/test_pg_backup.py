import pytest

from pg_backup.commands import CommandRunner, RestoreTestCommand, RunBackupCommand
from pg_backup.models import BackupConfig, BackupResult, BackupStatus
from pg_backup.validator import BackupValidator


def _make_config(db: str = "prod") -> BackupConfig:
    return BackupConfig(
        database_name=db,
        backup_dir="/backups",
        compress=True,
        retention_days=7,
    )


class TestBackupConfig:
    def test_defaults(self) -> None:
        cfg = _make_config()
        assert cfg.compress is True
        assert cfg.retention_days == 7
        assert cfg.max_parallel_jobs == 2

    def test_frozen(self) -> None:
        cfg = _make_config()
        with pytest.raises(AttributeError):
            cfg.database_name = "other"  # type: ignore[misc]


class TestBackupResult:
    def test_default_status(self) -> None:
        result = BackupResult()
        assert result.status == BackupStatus.SUCCESS

    def test_frozen(self) -> None:
        result = BackupResult()
        with pytest.raises(AttributeError):
            result.status = BackupStatus.FAILED  # type: ignore[misc]


class TestRunBackupCommand:
    def test_execute_success(self) -> None:
        cfg = _make_config()
        cmd = RunBackupCommand(cfg)
        result = cmd.execute()
        assert result.status == BackupStatus.SUCCESS
        assert result.file_path.endswith(".sql.gz")
        assert result.file_size_bytes > 0
        assert result.checksum != ""

    def test_description(self) -> None:
        cmd = RunBackupCommand(_make_config("mydb"))
        assert "mydb" in cmd.description()


class TestRestoreTestCommand:
    def test_execute_success(self) -> None:
        cfg = _make_config()
        cmd = RestoreTestCommand(cfg, "/backups/prod.sql.gz")
        result = cmd.execute()
        assert result.status == BackupStatus.SUCCESS

    def test_execute_failure(self) -> None:
        cfg = _make_config()
        cmd = RestoreTestCommand(cfg, "/backups/prod.sql.gz")
        cmd.set_fail(True)
        result = cmd.execute()
        assert result.status == BackupStatus.FAILED
        assert result.error_message is not None

    def test_description(self) -> None:
        cmd = RestoreTestCommand(_make_config(), "/backups/x.sql.gz")
        assert "/backups/x.sql.gz" in cmd.description()


class TestCommandRunner:
    def test_run_records_history(self) -> None:
        runner = CommandRunner()
        cmd = RunBackupCommand(_make_config())
        runner.run(cmd)
        assert len(runner.history) == 1
        assert runner.last_result() is not None

    def test_clear_history(self) -> None:
        runner = CommandRunner()
        runner.run(RunBackupCommand(_make_config()))
        runner.clear_history()
        assert len(runner.history) == 0

    def test_last_result_none_when_empty(self) -> None:
        runner = CommandRunner()
        assert runner.last_result() is None


class TestBackupValidator:
    def test_validate_backup_success(self) -> None:
        validator = BackupValidator()
        result = validator.validate_backup(_make_config())
        assert result.status == BackupStatus.SUCCESS
        assert len(validator.history) == 2

    def test_validate_with_failure(self) -> None:
        validator = BackupValidator()
        result = validator.validate_with_failure(_make_config())
        assert result.status == BackupStatus.FAILED

    def test_run_weekly_validation(self) -> None:
        validator = BackupValidator()
        configs = [_make_config("db1"), _make_config("db2"), _make_config("db3")]
        results = validator.run_weekly_validation(configs)
        assert len(results) == 3
        assert all(r.status == BackupStatus.SUCCESS for r in results)

    def test_integrity_check(self) -> None:
        validator = BackupValidator()
        ok_result = BackupResult(checksum="abc", file_size_bytes=100)
        assert validator._check_integrity(ok_result) is True
        bad_result = BackupResult(checksum="", file_size_bytes=0)
        assert validator._check_integrity(bad_result) is False

    def test_runner_injection(self) -> None:
        runner = CommandRunner()
        validator = BackupValidator(runner=runner)
        validator.validate_backup(_make_config())
        assert len(runner.history) == 2
