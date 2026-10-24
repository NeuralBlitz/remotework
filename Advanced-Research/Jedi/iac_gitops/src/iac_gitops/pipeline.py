from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from iac_gitops.models import DeploymentPhase, DeploymentState, GitOpsConfig


class PipelineStatus(str, Enum):
    IDLE = "Idle"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"


@dataclass
class PipelineStep:
    name: str
    status: str = "pending"
    duration_ms: int = 0
    output: str = ""


class GitOpsPipeline:
    def __init__(self, config: GitOpsConfig) -> None:
        self.config = config
        self._deployments: dict[str, DeploymentState] = {}
        self._status: PipelineStatus = PipelineStatus.IDLE
        self._steps: list[PipelineStep] = []
        self._sync_count: int = 0

    def register_app(self, app_name: str, target_revision: str) -> DeploymentState:
        state = DeploymentState(app_name=app_name, target_revision=target_revision)
        self._deployments[app_name] = state
        return state

    def run_sync(self) -> dict[str, DeploymentState]:
        self._status = PipelineStatus.RUNNING
        self._sync_count += 1

        self._steps = [
            PipelineStep(name="fetch_repo", status="completed", duration_ms=120),
            PipelineStep(name="diff_changes", status="completed", duration_ms=45),
            PipelineStep(name="apply_manifests", status="completed", duration_ms=200),
        ]

        for app_name, state in self._deployments.items():
            if state.target_revision:
                state.phase = DeploymentPhase.SYNCING
                state.current_revision = state.target_revision
                state.synced = True
                state.phase = DeploymentPhase.DEPLOYED

        self._status = PipelineStatus.COMPLETED
        return self._deployments

    def rollback(self, app_name: str, target_revision: str) -> bool:
        state = self._deployments.get(app_name)
        if state is None:
            return False
        state.phase = DeploymentPhase.ROLLBACK
        state.current_revision = target_revision
        state.phase = DeploymentPhase.DEPLOYED
        return True

    @property
    def status(self) -> PipelineStatus:
        return self._status

    @property
    def deployment_count(self) -> int:
        return len(self._deployments)

    @property
    def sync_count(self) -> int:
        return self._sync_count
