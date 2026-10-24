from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class BackupStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class BackupConfig:
    database_name: str
    backup_dir: str
    compress: bool = True
    include_schema: bool = True
    retention_days: int = 30
    max_parallel_jobs: int = 2


@dataclass(frozen=True)
class BackupResult:
    backup_id: UUID = field(default_factory=uuid4)
    config: BackupConfig | None = None
    status: BackupStatus = BackupStatus.SUCCESS
    file_path: str = ""
    file_size_bytes: int = 0
    checksum: str = ""
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
    error_message: str | None = None
    duration_seconds: float = 0.0
