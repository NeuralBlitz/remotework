from __future__ import annotations

import time

from .models import FailoverEvent, FailoverState


class FailoverStateMachine:
    def __init__(self) -> None:
        self._state = FailoverState.PRIMARY
        self._history: list[FailoverEvent] = []
        self._log_event("Initialized in PRIMARY state")

    @property
    def state(self) -> FailoverState:
        return self._state

    @property
    def history(self) -> list[FailoverEvent]:
        return list(self._history)

    def _log_event(self, message: str, error: str | None = None) -> None:
        self._history.append(
            FailoverEvent(
                state=self._state,
                timestamp=time.time(),
                message=message,
                error=error,
            )
        )

    def initiate_failover(self) -> None:
        if self._state != FailoverState.PRIMARY:
            msg = f"Cannot initiate failover from {self._state.value}"
            raise ValueError(msg)
        self._state = FailoverState.FAILING_OVER
        self._log_event("Failover initiated")

    def promote_standby(self) -> None:
        if self._state != FailoverState.FAILING_OVER:
            msg = f"Cannot promote standby from {self._state.value}"
            raise ValueError(msg)
        self._state = FailoverState.STANDBY_PROMOTED
        self._log_event("Standby promoted to primary")

    def start_rebuild(self) -> None:
        if self._state != FailoverState.STANDBY_PROMOTED:
            msg = f"Cannot start rebuild from {self._state.value}"
            raise ValueError(msg)
        self._state = FailoverState.REBUILDING
        self._log_event("Rebuild started")

    def complete_rebuild(self) -> None:
        if self._state != FailoverState.REBUILDING:
            msg = f"Cannot complete rebuild from {self._state.value}"
            raise ValueError(msg)
        self._state = FailoverState.PRIMARY
        self._log_event("Rebuild complete, back to PRIMARY")

    def can_transition(self, target: FailoverState) -> bool:
        transitions = {
            FailoverState.PRIMARY: {FailoverState.FAILING_OVER},
            FailoverState.FAILING_OVER: {FailoverState.STANDBY_PROMOTED},
            FailoverState.STANDBY_PROMOTED: {FailoverState.REBUILDING},
            FailoverState.REBUILDING: {FailoverState.PRIMARY},
        }
        return target in transitions.get(self._state, set())
