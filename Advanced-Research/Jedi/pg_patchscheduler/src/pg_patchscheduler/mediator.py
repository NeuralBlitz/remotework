from __future__ import annotations

from datetime import timedelta

from pg_patchscheduler.models import PatchStatus, PatchWindow


class PatchMediator:
    def __init__(self, min_gap: timedelta = timedelta(hours=1)) -> None:
        self._windows: list[PatchWindow] = []
        self._min_gap = min_gap

    def register_window(self, window: PatchWindow) -> None:
        self._windows.append(window)

    def resolve_conflicts(self) -> list[PatchWindow]:
        sorted_windows = sorted(self._windows, key=lambda w: w.start_time)
        resolved: list[PatchWindow] = []

        for window in sorted_windows:
            shifted = self._shift_if_conflict(window, resolved)
            shifted.status = PatchStatus.SCHEDULED
            resolved.append(shifted)

        self._windows = resolved
        return resolved

    def _shift_if_conflict(self, window: PatchWindow, resolved: list[PatchWindow]) -> PatchWindow:
        candidate = PatchWindow(
            provider=window.provider,
            instance_id=window.instance_id,
            start_time=window.start_time,
            duration=window.duration,
            patch_version=window.patch_version,
            status=window.status,
            priority=window.priority,
        )

        for existing in resolved:
            if candidate.overlaps(existing) or self._within_gap(candidate, existing):
                candidate = PatchWindow(
                    provider=candidate.provider,
                    instance_id=candidate.instance_id,
                    start_time=existing.end_time + self._min_gap,
                    duration=candidate.duration,
                    patch_version=candidate.patch_version,
                    status=candidate.status,
                    priority=candidate.priority,
                )

        return candidate

    def _within_gap(self, a: PatchWindow, b: PatchWindow) -> bool:
        if a.start_time >= b.end_time:
            return (a.start_time - b.end_time) < self._min_gap
        if b.start_time >= a.end_time:
            return (b.start_time - a.end_time) < self._min_gap
        return False

    def get_windows_by_provider(self, provider: str) -> list[PatchWindow]:
        return [w for w in self._windows if w.provider.value == provider]

    def get_deferred(self) -> list[PatchWindow]:
        return [w for w in self._windows if w.status == PatchStatus.DEFERRED]

    @property
    def window_count(self) -> int:
        return len(self._windows)
