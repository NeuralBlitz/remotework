from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class CloudProvider(Enum):
    AWS_RDS = "aws_rds"
    AZURE = "azure"
    ON_PREM = "on_prem"
    GCP_CLOUD_SQL = "gcp_cloud_sql"


class PatchStatus(Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    DEFERRED = "deferred"


@dataclass
class PatchWindow:
    provider: CloudProvider
    instance_id: str
    start_time: datetime
    duration: timedelta
    patch_version: str
    status: PatchStatus = PatchStatus.PENDING
    priority: int = 5

    @property
    def end_time(self) -> datetime:
        return self.start_time + self.duration

    def overlaps(self, other: PatchWindow) -> bool:
        return self.start_time < other.end_time and other.start_time < self.end_time


@dataclass(frozen=True)
class PatchResult:
    window: PatchWindow
    success: bool
    message: str
    applied_at: datetime = field(default_factory=datetime.now)
    previous_version: str = ""
    new_version: str = ""
