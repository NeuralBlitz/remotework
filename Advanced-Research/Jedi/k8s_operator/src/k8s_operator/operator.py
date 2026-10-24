from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from k8s_operator.models import PGCluster, ClusterPhase


@dataclass
class ReconcileResult:
    cluster_name: str
    changed: bool
    actions: list[str] = field(default_factory=list)
    error: str | None = None


class PGOperator:
    def __init__(self, reconcile_interval_seconds: int = 30) -> None:
        self.reconcile_interval = reconcile_interval_seconds
        self._clusters: dict[str, PGCluster] = {}
        self._hooks: list[Callable[[PGCluster], None]] = []

    def register_cluster(self, cluster: PGCluster) -> None:
        self._clusters[cluster.name] = cluster

    def unregister_cluster(self, name: str) -> None:
        self._clusters.pop(name, None)

    def add_hook(self, hook: Callable[[PGCluster], None]) -> None:
        self._hooks.append(hook)

    def reconcile(self, cluster_name: str) -> ReconcileResult:
        cluster = self._clusters.get(cluster_name)
        if cluster is None:
            return ReconcileResult(
                cluster_name=cluster_name, changed=False, error="Cluster not found"
            )

        actions: list[str] = []

        if cluster.status.phase == ClusterPhase.PENDING:
            cluster.status.phase = ClusterPhase.RUNNING
            cluster.status.ready_replicas = cluster.spec.replicas
            actions.append("initialized_cluster")

        if cluster.status.ready_replicas < cluster.spec.replicas:
            cluster.status.ready_replicas = cluster.spec.replicas
            actions.append("scaled_replicas")

        if not cluster.status.primary_node:
            cluster.status.primary_node = f"{cluster.name}-primary-0.{cluster.name}.svc"
            actions.append("assigned_primary")

        for hook in self._hooks:
            hook(cluster)

        changed = len(actions) > 0
        return ReconcileResult(cluster_name=cluster_name, changed=changed, actions=actions)

    def reconcile_all(self) -> list[ReconcileResult]:
        return [self.reconcile(name) for name in self._clusters]

    @property
    def cluster_count(self) -> int:
        return len(self._clusters)
