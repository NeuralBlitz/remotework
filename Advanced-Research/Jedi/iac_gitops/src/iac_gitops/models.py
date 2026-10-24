from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class DeploymentPhase(str, Enum):
    PENDING = "Pending"
    SYNCING = "Syncing"
    DEPLOYED = "Deployed"
    FAILED = "Failed"
    ROLLBACK = "Rollback"


@dataclass
class GitOpsConfig:
    repo_url: str
    branch: str = "main"
    path: str = "deploy/"
    auto_sync: bool = True
    prune: bool = True
    self_heal: bool = True
    sync_interval_seconds: int = 300
    target_namespace: str = "default"

    @property
    def full_path(self) -> str:
        return f"{self.repo_url}/{self.branch}/{self.path}"


@dataclass
class DeploymentState:
    app_name: str
    phase: DeploymentPhase = DeploymentPhase.PENDING
    current_revision: str = ""
    target_revision: str = ""
    synced: bool = False
    resources_count: int = 0
    healthy_count: int = 0
    message: str = ""

    @property
    def health_ratio(self) -> float:
        if self.resources_count == 0:
            return 0.0
        return self.healthy_count / self.resources_count

    def mark_synced(self, revision: str) -> None:
        self.current_revision = revision
        self.synced = True
        self.phase = DeploymentPhase.DEPLOYED
