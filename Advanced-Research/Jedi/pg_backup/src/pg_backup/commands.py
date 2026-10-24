from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4

from pg_backup.models import BackupConfig, BackupResult, BackupStatus


class BackupCommand(ABC):
    @abstractmethod
    def execute(self) -> BackupResult:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


class RunBackupCommand(BackupCommand):
    def __init__(self, config: BackupConfig) -> None:
        self._config = config

    def execute(self) -> BackupResult:
        started = datetime.now()
        file_name = f"{self._config.database_name}_{started.strftime('%Y%m%d_%H%M%S')}.sql.gz"
        path = f"{self._config.backup_dir}/{file_name}"
        mock_data = f"backup of {self._config.database_name}".encode()
        checksum = hashlib.sha256(mock_data).hexdigest()
        return BackupResult(
            backup_id=uuid4(),
            config=self._config,
            status=BackupStatus.SUCCESS,
            file_path=path,
            file_size_bytes=len(mock_data),
            checksum=checksum,
            started_at=started,
            completed_at=datetime.now(),
            duration_seconds=1.5,
        )

    def description(self) -> str:
        return f"Backup database {self._config.database_name}"


class RestoreTestCommand(BackupCommand):
    def __init__(self, config: BackupConfig, backup_file_path: str) -> None:
        self._config = config
        self._backup_file_path = backup_file_path
        self._fail: bool = False

    def execute(self) -> BackupResult:
        started = datetime.now()
        if self._fail:
            return BackupResult(
                config=self._config,
                status=BackupStatus.FAILED,
                file_path=self._backup_file_path,
                started_at=started,
                completed_at=datetime.now(),
                error_message="Restore failed: corrupted backup file",
                duration_seconds=0.5,
            )
        return BackupResult(
            config=self._config,
            status=BackupStatus.SUCCESS,
            file_path=self._backup_file_path,
            checksum="verified",
            started_at=started,
            completed_at=datetime.now(),
            duration_seconds=3.0,
        )

    def description(self) -> str:
        return f"Restore test from {self._backup_file_path}"

    def set_fail(self, fail: bool) -> None:
        self._fail = fail


class CommandRunner:
    def __init__(self) -> None:
        self._history: list[BackupResult] = []

    def run(self, command: BackupCommand) -> BackupResult:
        result = command.execute()
        self._history.append(result)
        return result

    @property
    def history(self) -> list[BackupResult]:
        return list(self._history)

    def last_result(self) -> BackupResult | None:
        return self._history[-1] if self._history else None

    def clear_history(self) -> None:
        self._history.clear()
