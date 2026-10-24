from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mediator import RegionMediator
    from .models import SyncEvent


class RegionSyncer:
    def __init__(self, region_name: str, mediator: RegionMediator) -> None:
        self._region_name = region_name
        self._mediator = mediator
        self._pending: list[dict[str, object]] = []
        self._synced_count = 0

    @property
    def region_name(self) -> str:
        return self._region_name

    @property
    def synced_count(self) -> int:
        return self._synced_count

    def queue_change(self, key: str, value: object) -> None:
        self._pending.append({"key": key, "value": value})

    def flush(self, target: str) -> list[SyncEvent]:
        events: list[SyncEvent] = []
        while self._pending:
            batch = self._pending[:100]
            self._pending = self._pending[100:]
            event = self._mediator.route_sync(self._region_name, target, len(batch))
            self._synced_count += len(batch)
            events.append(event)
        return events

    def sync_to(self, target: str, records: int) -> SyncEvent:
        event = self._mediator.route_sync(self._region_name, target, records)
        self._synced_count += records
        return event

    @property
    def pending_count(self) -> int:
        return len(self._pending)
