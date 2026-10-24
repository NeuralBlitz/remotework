"""Core data models for the HA cluster."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any


class NodeRole(str, enum.Enum):
    """Possible roles a node can have in the cluster."""

    LEADER = "leader"
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    STOPPED = "stopped"


class NodeStatus(str, enum.Enum):
    """Health status of a node."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNREACHABLE = "unreachable"
    UNKNOWN = "unknown"


@dataclass
class ClusterConfig:
    """Configuration for the HA cluster."""

    node_id: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    etcd_endpoints: list[str] = field(default_factory=lambda: ["http://localhost:2379"])
    health_check_interval: float = 5.0
    health_check_timeout: float = 3.0
    max_consecutive_failures: int = 3
    patroni_scope: str = "default"
    replication_slots: bool = True
    superuser_username: str = "postgres"
    replication_username: str = "replicator"


@dataclass
class NodeInfo:
    """Runtime information about a cluster node."""

    node_id: str
    role: NodeRole
    status: NodeStatus
    is_postgres_running: bool
    replication_lag_bytes: int
    last_health_check: float
    consecutive_failures: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_healthy(self) -> bool:
        return (
            self.status == NodeStatus.HEALTHY
            and self.is_postgres_running
            and self.consecutive_failures == 0
        )
