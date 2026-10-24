from __future__ import annotations

from .models import RegionNode, SyncEvent, SyncStatus


class RegionMediator:
    def __init__(self) -> None:
        self._regions: dict[str, RegionNode] = {}
        self._syncers: dict[str, object] = {}
        self._event_log: list[SyncEvent] = []

    def register_region(self, region: RegionNode) -> None:
        self._regions[region.name] = region

    def unregister_region(self, name: str) -> bool:
        if name not in self._regions:
            return False
        del self._regions[name]
        return True

    def get_region(self, name: str) -> RegionNode | None:
        return self._regions.get(name)

    def list_regions(self) -> list[RegionNode]:
        return [r for r in self._regions.values() if r.active]

    def notify_sync(self, event: SyncEvent) -> None:
        self._event_log.append(event)

    def get_events(self) -> list[SyncEvent]:
        return list(self._event_log)

    def resolve_conflict(self, event: SyncEvent, winner: str) -> SyncEvent:
        resolved = SyncEvent(
            source=event.source,
            target=event.target,
            status=SyncStatus.SYNCED,
            records_synced=event.records_synced,
            conflict_key=None,
        )
        self._event_log.append(resolved)
        return resolved

    def route_sync(self, source: str, target: str, records: int) -> SyncEvent:
        if source not in self._regions:
            msg = f"Source region '{source}' not found"
            raise KeyError(msg)
        if target not in self._regions:
            msg = f"Target region '{target}' not found"
            raise KeyError(msg)
        event = SyncEvent(
            source=source, target=target, status=SyncStatus.SYNCED, records_synced=records
        )
        self._event_log.append(event)
        return event
