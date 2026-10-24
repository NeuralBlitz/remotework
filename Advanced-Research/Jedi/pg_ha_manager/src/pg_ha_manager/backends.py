"""Backend abstractions — PostgreSQL operations and etcd election client."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from pg_ha_manager.models import ClusterConfig, NodeStatus

logger = logging.getLogger(__name__)


@dataclass
class HealthResult:
    """Result of a single health check."""

    status: NodeStatus
    is_postgres_running: bool
    replication_lag_bytes: int
    consecutive_failures: int

    @property
    def is_healthy(self) -> bool:
        return (
            self.status == NodeStatus.HEALTHY
            and self.is_postgres_running
            and self.consecutive_failures == 0
        )


class PgBackend:
    """Manages PostgreSQL process lifecycle and configuration.

    In production, this would shell out to `pg_ctl`, reload config
    via `pg_reload_conf()`, or talk to Patroni's REST API.
    """

    def __init__(self, config: ClusterConfig) -> None:
        self.config = config
        self._is_initialized = False
        self._is_running = False
        self._is_leader = False

    async def initialize(self) -> None:
        """Initialize the PostgreSQL data directory if needed."""
        logger.info("Initializing PostgreSQL backend at %s:%d",
                     self.config.postgres_host, self.config.postgres_port)
        self._is_initialized = True

    async def promote(self) -> None:
        """Promote this instance from standby to primary (pg_ctl promote)."""
        logger.info("Promoting PostgreSQL to primary")
        self._is_leader = True

    async def follow(self, leader_host: str, leader_port: int) -> None:
        """Configure this instance as a standby of the given leader.

        Sets `primary_conninfo` in postgresql.conf and creates a
        `standby.signal` file to signal standby mode.
        """
        logger.info("Configuring PostgreSQL to follow %s:%d", leader_host, leader_port)
        self._is_leader = False

    async def stop_accepting_writes(self) -> None:
        """Set the database to read-only mode (hot_standby = on)."""
        logger.info("Stopping write acceptance")

    async def shutdown(self) -> None:
        """Graceful shutdown (pg_ctl stop -m fast)."""
        logger.info("Shutting down PostgreSQL")
        self._is_running = False
        self._is_leader = False

    async def update_config(self, params: dict[str, str]) -> None:
        """Update postgresql.conf and reload."""
        logger.info("Updating config: %s", params)

    async def check_health(self) -> HealthResult:
        """Run pg_isready and check replication status.

        Returns a HealthResult with the current status.
        """
        try:
            # In production: subprocess.run(["pg_isready", ...])
            # or query pg_stat_replication, pg_wal_lsn_diff, etc.
            if not self._is_initialized:
                return HealthResult(
                    status=NodeStatus.UNREACHABLE,
                    is_postgres_running=False,
                    replication_lag_bytes=0,
                    consecutive_failures=1,
                )

            return HealthResult(
                status=NodeStatus.HEALTHY,
                is_postgres_running=True,
                replication_lag_bytes=0,
                consecutive_failures=0,
            )
        except Exception:
            return HealthResult(
                status=NodeStatus.UNREACHABLE,
                is_postgres_running=False,
                replication_lag_bytes=0,
                consecutive_failures=1,
            )


class ElectionClient:
    """etcd-based leader election client.

    Uses etcd leases for distributed leader election:
    - Acquire a lease with a TTL to become leader
    - Renew the lease periodically to maintain leadership
    - Watch for lease expiration to detect leader failure
    """

    def __init__(self, config: ClusterConfig) -> None:
        self.config = config
        self._connected = False
        self._has_lease = False
        self._leader_key = f"/pg_ha/{config.patroni_scope}/leader"
        self._lease_ttl = config.health_check_interval * 3

    async def connect(self) -> None:
        """Connect to etcd cluster."""
        logger.info("Connecting to etcd at %s", self.config.etcd_endpoints)
        self._connected = True

    async def disconnect(self) -> None:
        """Disconnect from etcd."""
        logger.info("Disconnecting from etcd")
        self._connected = False
        self._has_lease = False

    async def acquire_lease(self) -> bool:
        """Try to acquire the leader lease. Returns True if acquired."""
        if not self._connected:
            return False
        self._has_lease = True
        logger.info("Acquired leader lease for key %s", self._leader_key)
        return True

    async def release_lease(self) -> None:
        """Release the leader lease."""
        self._has_lease = False
        logger.info("Released leader lease")

    async def renew_lease(self) -> bool:
        """Renew the leader lease. Returns False if lease expired."""
        if not self._has_lease:
            return False
        logger.debug("Renewed leader lease")
        return True

    async def try_acquire_lease(self) -> bool:
        """Try to acquire the leader lease (non-blocking candidate attempt)."""
        return await self.acquire_lease()

    async def is_leader_alive(self) -> bool:
        """Check if the current leader's lease is still valid."""
        return self._has_lease

    async def get_current_leader(self) -> str | None:
        """Get the node_id of the current leader."""
        if self._has_lease:
            return self.config.node_id
        return None
