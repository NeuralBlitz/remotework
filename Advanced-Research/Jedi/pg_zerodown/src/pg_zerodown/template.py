from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import MigrationPhase, MigrationResult


class MigrationTemplate(ABC):
    def __init__(self) -> None:
        self._results: list[MigrationResult] = []
        self._dry_run = False
        self._current_phase: str = "not_started"

    @property
    def results(self) -> list[MigrationResult]:
        return list(self._results)

    @property
    def current_phase(self) -> str:
        return self._current_phase

    def set_dry_run(self, enabled: bool) -> None:
        self._dry_run = enabled

    def _record_result(self, result: MigrationResult) -> None:
        self._results.append(result)
        if not result.success:
            self._current_phase = f"failed_at_{result.phase.value}"
        elif result.phase.value == "contract":
            self._current_phase = "done"
        else:
            self._current_phase = result.phase.value

    def execute(self) -> list[MigrationResult]:
        self._results = []
        self._current_phase = "not_started"
        for phase_func in [self.expand, self.backfill, self.swap, self.contract]:
            before = len(self._results)
            result = phase_func()
            if len(self._results) == before:
                self._record_result(result)
            if not result.success:
                break
        return list(self._results)

    @abstractmethod
    def expand(self) -> MigrationResult: ...

    @abstractmethod
    def backfill(self) -> MigrationResult: ...

    @abstractmethod
    def swap(self) -> MigrationResult: ...

    @abstractmethod
    def contract(self) -> MigrationResult: ...
