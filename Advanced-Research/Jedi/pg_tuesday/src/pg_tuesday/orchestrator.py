from __future__ import annotations

from datetime import datetime
from typing import Protocol

from pg_tuesday.models import MaintenanceState, MaintenanceWindow, PatchResult
from pg_tuesday.states import MaintenanceStateMachine


class Patcher(Protocol):
    def drain(self, node_id: str) -> bool: ...
    def apply_patch(self, node_id: str) -> PatchResult: ...
    def verify(self, node_id: str) -> bool: ...


class MaintenanceOrchestrator:
    def __init__(self, window: MaintenanceWindow, patcher: Patcher) -> None:
        self._window = window
        self._patcher = patcher
        self._state_machine = MaintenanceStateMachine(window)

    @property
    def window(self) -> MaintenanceWindow:
        return self._window

    @property
    def state(self) -> MaintenanceState:
        return self._state_machine.current_state

    def drain_traffic(self, active_connections: int = 0) -> MaintenanceState:
        if not self._state_machine.guard_drain(active_connections):
            raise RuntimeError(
                f"Cannot drain: state={self.state.value}, active_connections={active_connections}"
            )
        self._state_machine.transition(MaintenanceState.DRAINING_TRAFFIC)
        self._window.started_at = datetime.now()
        return self.state

    def apply_patches(self) -> MaintenanceState:
        if not self._state_machine.guard_patch():
            raise RuntimeError(f"Cannot patch: state={self.state.value}")
        self._state_machine.transition(MaintenanceState.PATCHING)
        for node_id in self._window.node_ids:
            result = self._patcher.apply_patch(node_id)
            self._window.patch_results.append(result)
        self._state_machine.transition(MaintenanceState.VERIFYING)
        return self.state

    def verify_and_complete(self) -> MaintenanceState:
        if not self._state_machine.guard_verify():
            raise RuntimeError(f"Cannot verify: state={self.state.value}")
        for node_id in self._window.node_ids:
            if not self._patcher.verify(node_id):
                self._state_machine.transition(MaintenanceState.FAILED)
                return self.state
        if self._state_machine.guard_complete():
            self._state_machine.transition(MaintenanceState.COMPLETED)
            self._window.completed_at = datetime.now()
        else:
            self._state_machine.transition(MaintenanceState.FAILED)
        return self.state

    def run_full_workflow(self, active_connections: int = 0) -> MaintenanceState:
        self.drain_traffic(active_connections)
        self.apply_patches()
        self.verify_and_complete()
        return self.state
