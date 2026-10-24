from __future__ import annotations

from pg_backup.commands import CommandRunner, RestoreTestCommand, RunBackupCommand
from pg_backup.models import BackupConfig, BackupResult, BackupStatus


class BackupValidator:
    def __init__(self, runner: CommandRunner | None = None) -> None:
        self._runner = runner or CommandRunner()

    def validate_backup(self, config: BackupConfig) -> BackupResult:
        backup_cmd = RunBackupCommand(config)
        backup_result = self._runner.run(backup_cmd)
        if backup_result.status != BackupStatus.SUCCESS:
            return backup_result
        restore_cmd = RestoreTestCommand(config, backup_result.file_path)
        restore_result = self._runner.run(restore_cmd)
        if restore_result.status != BackupStatus.SUCCESS:
            return restore_result
        if not self._check_integrity(backup_result):
            return BackupResult(
                config=config,
                status=BackupStatus.FAILED,
                file_path=backup_result.file_path,
                error_message="Integrity check failed: checksum mismatch",
            )
        return backup_result

    def validate_with_failure(self, config: BackupConfig) -> BackupResult:
        backup_cmd = RunBackupCommand(config)
        backup_result = self._runner.run(backup_cmd)
        restore_cmd = RestoreTestCommand(config, backup_result.file_path)
        restore_cmd.set_fail(True)
        restore_result = self._runner.run(restore_cmd)
        return restore_result

    def run_weekly_validation(self, configs: list[BackupConfig]) -> list[BackupResult]:
        results: list[BackupResult] = []
        for config in configs:
            result = self.validate_backup(config)
            results.append(result)
        return results

    def _check_integrity(self, backup: BackupResult) -> bool:
        return bool(backup.checksum) and backup.file_size_bytes > 0

    @property
    def history(self) -> list[BackupResult]:
        return self._runner.history
