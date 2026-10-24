from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import FailoverEvent
from .states import FailoverStateMachine


class FailoverManager:
    def __init__(self) -> None:
        self._machines: dict[str, FailoverStateMachine] = {}
        self._cooldown_seconds = 60.0
        self._last_failover: dict[str, float] = {}

    def register_cluster(self, name: str) -> FailoverStateMachine:
        if name in self._machines:
            msg = f"Cluster '{name}' already registered"
            raise ValueError(msg)
        machine = FailoverStateMachine()
        self._machines[name] = machine
        return machine

    def get_cluster(self, name: str) -> FailoverStateMachine:
        if name not in self._machines:
            msg = f"Cluster '{name}' not found"
            raise KeyError(msg)
        return self._machines[name]

    def execute_failover(self, name: str) -> list[FailoverEvent]:
        machine = self.get_cluster(name)
        now = time.time()
        last = self._last_failover.get(name, 0.0)
        if now - last < self._cooldown_seconds:
            msg = f"Cooldown active for cluster '{name}'"
            raise RuntimeError(msg)

        machine.initiate_failover()
        machine.promote_standby()
        machine.start_rebuild()
        machine.complete_rebuild()
        self._last_failover[name] = now
        return machine.history

    def list_clusters(self) -> list[str]:
        return list(self._machines.keys())

    def set_cooldown(self, seconds: float) -> None:
        if seconds < 0:
            msg = "Cooldown must be non-negative"
            raise ValueError(msg)
        self._cooldown_seconds = seconds
