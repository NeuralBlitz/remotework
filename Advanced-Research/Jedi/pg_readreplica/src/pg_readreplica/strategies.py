from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import ReplicaNode, ReplicaRegion


class RoutingStrategy(ABC):
    @abstractmethod
    def select(
        self, replicas: list[ReplicaNode], reader_region: ReplicaRegion
    ) -> ReplicaNode | None: ...

    @property
    @abstractmethod
    def name(self) -> str: ...


class NearestReplicaStrategy(RoutingStrategy):
    _REGION_DISTANCES: dict[tuple[ReplicaRegion, ReplicaRegion], float] = {}

    @property
    def name(self) -> str:
        return "nearest"

    def set_region_distance(self, r1: ReplicaRegion, r2: ReplicaRegion, distance: float) -> None:
        self._REGION_DISTANCES[(r1, r2)] = distance
        self._REGION_DISTANCES[(r2, r1)] = distance

    def _get_distance(self, reader: ReplicaRegion, replica: ReplicaRegion) -> float:
        if reader == replica:
            return 0.0
        return self._REGION_DISTANCES.get((reader, replica), 1000.0)

    def select(
        self, replicas: list[ReplicaNode], reader_region: ReplicaRegion
    ) -> ReplicaNode | None:
        healthy = [r for r in replicas if r.healthy]
        if not healthy:
            return None
        return min(healthy, key=lambda r: self._get_distance(reader_region, r.region))


class LatencyBasedStrategy(RoutingStrategy):
    @property
    def name(self) -> str:
        return "latency"

    def select(
        self, replicas: list[ReplicaNode], reader_region: ReplicaRegion
    ) -> ReplicaNode | None:
        _ = reader_region
        healthy = [r for r in replicas if r.healthy]
        if not healthy:
            return None
        return min(healthy, key=lambda r: r.latency_ms)


class RoundRobinStrategy(RoutingStrategy):
    def __init__(self) -> None:
        self._index = 0

    @property
    def name(self) -> str:
        return "round_robin"

    def select(
        self, replicas: list[ReplicaNode], reader_region: ReplicaRegion
    ) -> ReplicaNode | None:
        _ = reader_region
        healthy = [r for r in replicas if r.healthy]
        if not healthy:
            return None
        node = healthy[self._index % len(healthy)]
        self._index += 1
        return node
