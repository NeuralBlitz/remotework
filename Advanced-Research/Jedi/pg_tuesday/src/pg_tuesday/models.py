from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class MaintenanceState(Enum):
    SCHEDULED = "scheduled"
    DRAINING_TRAFFIC = "draining_traffic"
    PATCHING = "patching"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class PatchResult:
    node_id: str
    success: bool
    pre_patch_version: str
    post_patch_version: str
    duration_seconds: float
    error_message: str | None = None


@dataclass
class MaintenanceWindow:
    window_id: UUID = field(default_factory=uuid4)
    scheduled_at: datetime = field(default_factory=datetime.now)
    state: MaintenanceState = MaintenanceState.SCHEDULED
    node_ids: list[str] = field(default_factory=list)
    patch_results: list[PatchResult] = field(default_factory=list)
    started_at: datetime | None = None
    completed_at: datetime | None = None

    def all_nodes_patched(self) -> bool:
        return len(self.patch_results) == len(self.node_ids) and all(
            r.success for r in self.patch_results
        )

    def has_failures(self) -> bool:
        return any(not r.success for r in self.patch_results)
