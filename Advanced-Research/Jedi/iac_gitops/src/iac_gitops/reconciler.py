from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from iac_gitops.models import DeploymentPhase, DeploymentState, GitOpsConfig
from iac_gitops.pipeline import GitOpsPipeline


@dataclass
class ReconcileResult:
    app_name: str
    action: str
    success: bool
    message: str = ""


class GitOpsReconciler:
    def __init__(self, pipeline: GitOpsPipeline) -> None:
        self.pipeline = pipeline
        self._desired_states: dict[str, str] = {}
        self._reconcile_log: list[ReconcileResult] = []
        self._observers: list[Callable[[ReconcileResult], None]] = []

    def set_desired_state(self, app_name: str, revision: str) -> None:
        self._desired_states[app_name] = revision

    def add_observer(self, observer: Callable[[ReconcileResult], None]) -> None:
        self._observers.append(observer)

    def reconcile(self, app_name: str) -> ReconcileResult:
        state = self.pipeline._deployments.get(app_name)
        desired = self._desired_states.get(app_name)

        if state is None:
            result = ReconcileResult(
                app_name=app_name, action="error", success=False, message="App not found"
            )
        elif desired is None:
            result = ReconcileResult(
                app_name=app_name, action="skip", success=True, message="No desired state"
            )
        elif state.current_revision != desired:
            state.phase = DeploymentPhase.SYNCING
            state.current_revision = desired
            state.synced = True
            state.phase = DeploymentPhase.DEPLOYED
            result = ReconcileResult(app_name=app_name, action="sync", success=True)
        else:
            result = ReconcileResult(
                app_name=app_name, action="noop", success=True, message="Already synced"
            )

        self._reconcile_log.append(result)
        for obs in self._observers:
            obs(result)

        return result

    def reconcile_all(self) -> list[ReconcileResult]:
        results = []
        for app_name in self._desired_states:
            results.append(self.reconcile(app_name))
        return results

    @property
    def reconcile_count(self) -> int:
        return len(self._reconcile_log)

    @property
    def desired_state_count(self) -> int:
        return len(self._desired_states)
