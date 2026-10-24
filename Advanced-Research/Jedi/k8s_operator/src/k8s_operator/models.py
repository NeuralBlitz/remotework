from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ClusterPhase(str, Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    FAILED = "Failed"
    TERMINATING = "Terminating"


@dataclass
class PGClusterSpec:
    replicas: int = 3
    storage_size_gb: int = 100
    version: str = "16.2"
    cpu_limit: str = "2"
    memory_limit: str = "4Gi"
    enable_ssl: bool = True
    max_connections: int = 200


@dataclass
class PGClusterStatus:
    phase: ClusterPhase = ClusterPhase.PENDING
    ready_replicas: int = 0
    primary_node: str = ""
    last_reconcile: str = ""
    conditions: list[str] = field(default_factory=list)


@dataclass
class PGCluster:
    name: str
    namespace: str
    spec: PGClusterSpec = field(default_factory=PGClusterSpec)
    status: PGClusterStatus = field(default_factory=PGClusterStatus)
    labels: dict[str, str] = field(default_factory=dict)

    @property
    def is_ready(self) -> bool:
        return (
            self.status.phase == ClusterPhase.RUNNING
            and self.status.ready_replicas >= self.spec.replicas
        )

    def add_label(self, key: str, value: str) -> None:
        self.labels[key] = value
