"""Node manager — orchestrates state transitions, health checks, and election."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any

from pg_ha_manager.backends import ElectionClient, PgBackend
from pg_ha_manager.health import HealthChecker
from pg_ha_manager.models import ClusterConfig, NodeInfo, NodeRole
from pg_ha_manager.states import Follower, NodeState, Stopped

logger = logging.getLogger(__name__)


class NodeManager:
    """Main orchestrator that owns the state and drives reconciliation loops.

    Usage::

        config = ClusterConfig(node_id="node-1")
        manager = NodeManager(config)
        await manager.start()          # enters Candidate, then Leader or Follower
        await manager.stop()           # graceful shutdown
    """

    def __init__(
        self,
        config: ClusterConfig,
        pg_backend: PgBackend | None = None,
        election_client: ElectionClient | None = None,
        health_checker: HealthChecker | None = None,
    ) -> None:
        self.config = config
        self.pg_backend = pg_backend or PgBackend(config)
        self.election_client = election_client or ElectionClient(config)
        self.health_checker = health_checker or HealthChecker(config, self.pg_backend)

        self._state: NodeState = Stopped()
        self._running = False
        self._reconcile_task: asyncio.Task[Any] | None = None
        self._on_transition_callbacks: list[Any] = []

    @property
    def state(self) -> NodeState:
        return self._state

    @property
    def role(self) -> NodeRole:
        return NodeRole(self._state.role())

    def on_transition(self, callback: Any) -> None:
        """Register a callback called on every state transition."""
        self._on_transition_callbacks.append(callback)

    async def start(self) -> None:
        """Start the manager — begins reconciliation loop."""
        logger.info("Starting node manager for %s", self.config.node_id)
        self._running = True
        await self.pg_backend.initialize()
        await self.election_client.connect()

        initial_state = Follower()
        await self.transition_to(initial_state)

        self._reconcile_task = asyncio.create_task(self._reconcile_loop())

    async def stop(self) -> None:
        """Gracefully stop the manager."""
        logger.info("Stopping node manager for %s", self.config.node_id)
        self._running = False

        if self._reconcile_task:
            self._reconcile_task.cancel()
            try:
                await self._reconcile_task
            except asyncio.CancelledError:
                pass

        await self.transition_to(Stopped())
        await self.election_client.disconnect()
        await self.pg_backend.shutdown()

    async def transition_to(self, new_state: NodeState) -> None:
        """Transition to a new state."""
        if type(new_state) is type(self._state):
            return

        old_role = self._state.role()
        await self._state.exit(self)

        self._state = new_state
        await self._state.enter(self)

        new_role = new_state.role()
        logger.info("State transition: %s -> %s", old_role, new_role)

        for callback in self._on_transition_callbacks:
            try:
                callback(old_role, new_role)
            except Exception:
                logger.exception("Transition callback failed")

    async def reconcile(self) -> None:
        """Run one reconciliation cycle."""
        await self._state.reconcile(self)

    async def get_node_info(self) -> NodeInfo:
        """Get current node information."""
        health = await self.health_checker.check_self()
        return NodeInfo(
            node_id=self.config.node_id,
            role=self.role,
            status=health.status,
            is_postgres_running=health.is_postgres_running,
            replication_lag_bytes=health.replication_lag_bytes,
            last_health_check=time.time(),
            consecutive_failures=health.consecutive_failures,
        )

    def _build_sync_standby_names(self) -> str:
        """Build synchronous_standby_names for replication config."""
        return f"FIRST 1 ({self.config.replication_username})"

    async def _reconcile_loop(self) -> None:
        """Background loop that drives reconciliation."""
        while self._running:
            try:
                await self.reconcile()
            except Exception:
                logger.exception("Reconciliation error")
            await asyncio.sleep(self.config.health_check_interval)
