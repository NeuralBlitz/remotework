from __future__ import annotations

from typing import TYPE_CHECKING

from pg_tuesday.models import MaintenanceState

if TYPE_CHECKING:
    from pg_tuesday.models import MaintenanceWindow

TRANSITIONS: dict[MaintenanceState, set[MaintenanceState]] = {
    MaintenanceState.SCHEDULED: {MaintenanceState.DRAINING_TRAFFIC},
    MaintenanceState.DRAINING_TRAFFIC: {MaintenanceState.PATCHING},
    MaintenanceState.PATCHING: {MaintenanceState.VERIFYING, MaintenanceState.FAILED},
    MaintenanceState.VERIFYING: {MaintenanceState.COMPLETED, MaintenanceState.FAILED},
    MaintenanceState.COMPLETED: set(),
    MaintenanceState.FAILED: set(),
}


class InvalidTransitionError(Exception):
    pass


class MaintenanceStateMachine:
    def __init__(self, window: MaintenanceWindow) -> None:
        self._window = window

    @property
    def current_state(self) -> MaintenanceState:
        return self._window.state

    def allowed_transitions(self) -> set[MaintenanceState]:
        return TRANSITIONS.get(self.current_state, set())

    def transition(self, target: MaintenanceState) -> MaintenanceState:
        allowed = self.allowed_transitions()
        if target not in allowed:
            raise InvalidTransitionError(
                f"Cannot transition from {self.current_state.value} to {target.value}. "
                f"Allowed: {[s.value for s in allowed]}"
            )
        self._window.state = target
        return target

    def guard_drain(self, active_connections: int) -> bool:
        if self.current_state != MaintenanceState.SCHEDULED:
            return False
        return active_connections == 0

    def guard_patch(self) -> bool:
        return self.current_state == MaintenanceState.DRAINING_TRAFFIC

    def guard_verify(self) -> bool:
        return self.current_state == MaintenanceState.VERIFYING

    def guard_complete(self) -> bool:
        if self.current_state != MaintenanceState.VERIFYING:
            return False
        return self._window.all_nodes_patched()
