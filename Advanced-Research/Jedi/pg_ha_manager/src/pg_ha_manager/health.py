"""Health checking — monitors node and cluster health."""

from __future__ import annotations

import logging
import time

from pg_ha_manager.backends import HealthResult, PgBackend
from pg_ha_manager.models import ClusterConfig, NodeStatus

logger = logging.getLogger(__name__)


class HealthChecker:
    """Periodic health checks for local node and cluster peers.

    Checks:
    1. PostgreSQL process health (pg_isready)
    2. Replication lag (pg_stat_replication)
    3. Disk space, CPU, memory (via psutil in production)
    4. Consecutive failure tracking for state transitions
    """

    def __init__(self, config: ClusterConfig, pg_backend: PgBackend) -> None:
        self.config = config
        self.pg_backend = pg_backend
        self._consecutive_failures = 0
        self._last_check_time: float = 0

    async def check_self(self) -> HealthResult:
        """Run a health check on the local node."""
        result = await self.pg_backend.check_health()

        if result.status == NodeStatus.UNREACHABLE:
            self._consecutive_failures += 1
        else:
            self._consecutive_failures = 0

        self._last_check_time = time.time()

        if self._consecutive_failures >= self.config.max_consecutive_failures:
            logger.error(
                "Node %s has %d consecutive failures",
                self.config.node_id,
                self._consecutive_failures,
            )

        return HealthResult(
            status=result.status,
            is_postgres_running=result.is_postgres_running,
            replication_lag_bytes=result.replication_lag_bytes,
            consecutive_failures=self._consecutive_failures,
        )

    @property
    def consecutive_failures(self) -> int:
        return self._consecutive_failures
