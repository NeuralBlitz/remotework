from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from k8s_operator.models import PGCluster
from k8s_operator.operator import PGOperator


@dataclass
class ResourceEvent:
    event_type: str
    resource_name: str
    namespace: str
    payload: dict[str, Any] = field(default_factory=dict)


class ResourceController:
    def __init__(self, operator: PGOperator) -> None:
        self.operator = operator
        self._event_log: list[ResourceEvent] = []
        self._running = False

    def handle_event(self, event: ResourceEvent) -> bool:
        self._event_log.append(event)

        if event.event_type == "ADD":
            spec_data = event.payload.get("spec", {})
            cluster = PGCluster(
                name=event.resource_name,
                namespace=event.namespace,
            )
            cluster.spec.replicas = spec_data.get("replicas", 3)
            self.operator.register_cluster(cluster)
            return True

        if event.event_type == "DELETE":
            self.operator.unregister_cluster(event.resource_name)
            return True

        if event.event_type == "UPDATE":
            result = self.operator.reconcile(event.resource_name)
            return result.changed

        return False

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def event_count(self) -> int:
        return len(self._event_log)
