from __future__ import annotations

from typing import TYPE_CHECKING

from .strategies import RoutingStrategy

if TYPE_CHECKING:
    from .models import ReplicaNode, ReplicaRegion, RouteDecision


class ReplicaRouter:
    def __init__(self, strategy: RoutingStrategy | None = None) -> None:
        self._replicas: list[ReplicaNode] = []
        self._strategy = strategy

    @property
    def strategy(self) -> RoutingStrategy | None:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: RoutingStrategy) -> None:
        self._strategy = strategy

    def add_replica(self, replica: ReplicaNode) -> None:
        if replica not in self._replicas:
            self._replicas.append(replica)

    def remove_replica(self, name: str) -> bool:
        for i, r in enumerate(self._replicas):
            if r.name == name:
                self._replicas.pop(i)
                return True
        return False

    def list_replicas(self) -> list[ReplicaNode]:
        return list(self._replicas)

    def route(self, reader_region: ReplicaRegion) -> RouteDecision | None:
        if not self._strategy or not self._replicas:
            return None
        node = self._strategy.select(self._replicas, reader_region)
        if node is None:
            return None
        from .models import RouteDecision

        return RouteDecision(
            node=node,
            strategy=self._strategy.name,
            latency_ms=node.latency_ms,
            score=max(0.0, 100.0 - node.latency_ms),
        )
