from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pg_patchscheduler.models import PatchResult, PatchWindow

from pg_patchscheduler.mediator import PatchMediator
from pg_patchscheduler.models import PatchResult, PatchStatus


class PatchScheduler:
    def __init__(self, mediator: PatchMediator | None = None) -> None:
        self._mediator = mediator or PatchMediator()
        self._results: list[PatchResult] = []

    def add_window(self, window: PatchWindow) -> None:
        self._mediator.register_window(window)

    def schedule_all(self) -> list[PatchWindow]:
        return self._mediator.resolve_conflicts()

    def execute_patch(self, window: PatchWindow) -> PatchResult:
        window.status = PatchStatus.IN_PROGRESS
        try:
            result = PatchResult(
                window=window,
                success=True,
                message=f"Patched {window.instance_id} to {window.patch_version}",
                applied_at=datetime.now(),
                new_version=window.patch_version,
            )
            window.status = PatchStatus.COMPLETED
        except Exception as exc:
            result = PatchResult(
                window=window,
                success=False,
                message=str(exc),
                applied_at=datetime.now(),
            )
            window.status = PatchStatus.FAILED
        self._results.append(result)
        return result

    def execute_all(self) -> list[PatchResult]:
        self.schedule_all()
        results: list[PatchResult] = []
        for window in self._mediator._windows:
            results.append(self.execute_patch(window))
        return results

    @property
    def results(self) -> list[PatchResult]:
        return list(self._results)

    @property
    def mediator(self) -> PatchMediator:
        return self._mediator
