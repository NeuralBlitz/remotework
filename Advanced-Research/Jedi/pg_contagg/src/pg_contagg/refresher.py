from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from pg_contagg.models import AggregateState, RefreshConfig
from pg_contagg.states import AggregateStateMachine


@dataclass
class RefreshResult:
    view_name: str
    success: bool
    state: AggregateState
    refresh_count: int
    duration_ms: float = 0.0
    error: str | None = None


class AggregateRefresher:
    def __init__(self) -> None:
        self._machines: dict[str, AggregateStateMachine] = {}
        self._history: list[RefreshResult] = []

    def register(self, config: RefreshConfig) -> AggregateStateMachine:
        if config.view_name in self._machines:
            raise ValueError(f"Already registered: {config.view_name}")
        machine = AggregateStateMachine(config)
        self._machines[config.view_name] = machine
        return machine

    def unregister(self, view_name: str) -> bool:
        if view_name not in self._machines:
            raise KeyError(f"Not registered: {view_name}")
        del self._machines[view_name]
        return True

    def refresh(self, view_name: str, now: datetime | None = None) -> RefreshResult:
        now = now or datetime.now()
        machine = self._machines.get(view_name)
        if machine is None:
            raise KeyError(f"Not registered: {view_name}")
        if not machine.can_refresh():
            return RefreshResult(
                view_name=view_name,
                success=False,
                state=machine.state,
                refresh_count=machine.refresh_count,
                error=f"Cannot refresh in state: {machine.state.value}",
            )
        machine.start_refresh(now)
        try:
            machine.complete_refresh(now)
            result = RefreshResult(
                view_name=view_name,
                success=True,
                state=machine.state,
                refresh_count=machine.refresh_count,
            )
        except Exception as e:
            machine.fail_refresh(str(e))
            result = RefreshResult(
                view_name=view_name,
                success=False,
                state=machine.state,
                refresh_count=machine.refresh_count,
                error=str(e),
            )
        self._history.append(result)
        return result

    def mark_all_stale(self) -> int:
        count = 0
        for machine in self._machines.values():
            if machine.state == AggregateState.CURRENT:
                machine.mark_stale()
                count += 1
        return count

    def get_state(self, view_name: str) -> AggregateState | None:
        machine = self._machines.get(view_name)
        return machine.state if machine else None

    def get_machine(self, view_name: str) -> AggregateStateMachine | None:
        return self._machines.get(view_name)

    def list_views(self) -> list[str]:
        return list(self._machines.keys())

    def get_history(self) -> list[RefreshResult]:
        return list(self._history)

    def refresh_all(self, now: datetime | None = None) -> list[RefreshResult]:
        results = []
        for view_name in self._machines:
            if self._machines[view_name].can_refresh():
                results.append(self.refresh(view_name, now))
        return results

    def get_stale_views(self) -> list[str]:
        return [k for k, v in self._machines.items() if v.state == AggregateState.STALE]
