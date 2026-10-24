from __future__ import annotations

from typing import Callable

from pg_contagg.models import AggregateState, RefreshConfig


class AggregateStateMachine:
    def __init__(self, config: RefreshConfig) -> None:
        if not config.validate():
            raise ValueError(f"Invalid config: {config.view_name}")
        self._config = config
        self._state = AggregateState.STALE
        self._refresh_count = 0
        self._last_refresh: datetime | None = None
        self._error_message: str | None = None
        self._listeners: list[Callable[[AggregateState, AggregateState], None]] = []

    @property
    def state(self) -> AggregateState:
        return self._state

    @property
    def config(self) -> RefreshConfig:
        return self._config

    @property
    def refresh_count(self) -> int:
        return self._refresh_count

    @property
    def last_refresh(self) -> datetime | None:
        return self._last_refresh

    @property
    def error_message(self) -> str | None:
        return self._error_message

    def add_listener(self, callback: Callable[[AggregateState, AggregateState], None]) -> None:
        self._listeners.append(callback)

    def _transition(self, new_state: AggregateState) -> None:
        old_state = self._state
        self._state = new_state
        for listener in self._listeners:
            listener(old_state, new_state)

    def start_refresh(self, now: datetime) -> bool:
        if self._state == AggregateState.REFRESHING:
            raise RuntimeError("Refresh already in progress")
        self._error_message = None
        self._transition(AggregateState.REFRESHING)
        return True

    def complete_refresh(self, now: datetime) -> bool:
        if self._state != AggregateState.REFRESHING:
            raise RuntimeError("No refresh in progress")
        self._refresh_count += 1
        self._last_refresh = now
        self._transition(AggregateState.CURRENT)
        return True

    def fail_refresh(self, error: str) -> bool:
        if self._state != AggregateState.REFRESHING:
            raise RuntimeError("No refresh in progress")
        self._error_message = error
        self._transition(AggregateState.ERROR)
        return True

    def mark_stale(self) -> bool:
        if self._state == AggregateState.REFRESHING:
            raise RuntimeError("Cannot mark stale while refreshing")
        self._transition(AggregateState.STALE)
        return True

    def reset(self) -> None:
        self._state = AggregateState.STALE
        self._refresh_count = 0
        self._last_refresh = None
        self._error_message = None

    def can_refresh(self) -> bool:
        return self._state in (AggregateState.STALE, AggregateState.CURRENT, AggregateState.ERROR)
