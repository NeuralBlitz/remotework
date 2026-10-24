"""State Pattern implementation for node roles."""

from __future__ import annotations

import abc
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pg_ha_manager.node import NodeManager

logger = logging.getLogger(__name__)


class NodeState(abc.ABC):
    """Abstract base class for all node states."""

    @abc.abstractmethod
    async def enter(self, manager: NodeManager) -> None:
        """Called when entering this state."""
        ...

    @abc.abstractmethod
    async def exit(self, manager: NodeManager) -> None:
        """Called when exiting this state."""
        ...

    @abc.abstractmethod
    async def reconcile(self, manager: NodeManager) -> None:
        """Check current state and decide if transition is needed."""
        ...

    @abc.abstractmethod
    def role(self) -> str:
        """Return the role name for this state."""
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Leader(NodeState):
    """Leader state — this node is the primary PostgreSQL instance.

    Responsibilities:
    - Accept all read/write traffic
    - Send heartbeats to etcd to maintain leadership
    - Monitor self-health; demote to Candidate if unhealthy
    - Watch for other nodes requesting leadership
    """

    async def enter(self, manager: NodeManager) -> None:
        logger.info("Entering LEADER state on node %s", manager.config.node_id)
        await manager.pg_backend.promote()
        await manager.election_client.acquire_lease()
        await manager.pg_backend.update_config(
            {"synchronous_standby_names": manager._build_sync_standby_names()}
        )

    async def exit(self, manager: NodeManager) -> None:
        logger.info("Exiting LEADER state on node %s", manager.config.node_id)
        await manager.election_client.release_lease()

    async def reconcile(self, manager: NodeManager) -> None:
        health = await manager.health_checker.check_self()
        if not health.is_healthy:
            logger.warning("Leader %s is unhealthy, demoting", manager.config.node_id)
            await manager.transition_to(Candidate())
            return

        await manager.election_client.renew_lease()
        logger.debug("Leader %s heartbeat renewed", manager.config.node_id)

    def role(self) -> str:
        return "leader"


class Follower(NodeState):
    """Follower state — this node is a read replica.

    Responsibilities:
    - Accept only read traffic
    - Monitor replication lag
    - Watch for leader health via etcd
    - Transition to Candidate if leader disappears
    """

    async def enter(self, manager: NodeManager) -> None:
        logger.info("Entering FOLLOWER state on node %s", manager.config.node_id)
        await manager.pg_backend.follow(
            leader_host=manager.config.postgres_host,
            leader_port=manager.config.postgres_port,
        )

    async def exit(self, manager: NodeManager) -> None:
        logger.info("Exiting FOLLOWER state on node %s", manager.config.node_id)

    async def reconcile(self, manager: NodeManager) -> None:
        leader_alive = await manager.election_client.is_leader_alive()
        if not leader_alive:
            logger.info("Leader is dead, promoting %s to CANDIDATE", manager.config.node_id)
            await manager.transition_to(Candidate())
            return

        health = await manager.health_checker.check_self()
        if health.replication_lag_bytes > 100 * 1024 * 1024:
            logger.warning(
                "Follower %s replication lag too high: %d bytes",
                manager.config.node_id,
                health.replication_lag_bytes,
            )

    def role(self) -> str:
        return "follower"


class Candidate(NodeState):
    """Candidate state — this node is competing for leadership.

    Responsibilities:
    - Attempt to acquire the leader lease from etcd
    - Verify self is healthy enough to lead
    - If elected, transition to Leader
    - If another node wins, transition to Follower
    - Implement randomized backoff to avoid split-brain
    """

    async def enter(self, manager: NodeManager) -> None:
        logger.info("Entering CANDIDATE state on node %s", manager.config.node_id)
        await manager.pg_backend.stop_accepting_writes()

    async def exit(self, manager: NodeManager) -> None:
        logger.info("Exiting CANDIDATE state on node %s", manager.config.node_id)

    async def reconcile(self, manager: NodeManager) -> None:
        health = await manager.health_checker.check_self()
        if not health.is_healthy:
            logger.info("Candidate %s is unhealthy, staying candidate", manager.config.node_id)
            return

        won = await manager.election_client.try_acquire_lease()
        if won:
            logger.info("Candidate %s won election, becoming LEADER", manager.config.node_id)
            await manager.transition_to(Leader())
        else:
            current_leader = await manager.election_client.get_current_leader()
            if current_leader and current_leader != manager.config.node_id:
                logger.info(
                    "Candidate %s lost election to %s, becoming FOLLOWER",
                    manager.config.node_id,
                    current_leader,
                )
                await manager.transition_to(Follower())

    def role(self) -> str:
        return "candidate"


class Stopped(NodeState):
    """Stopped state — node is offline or being shut down."""

    async def enter(self, manager: NodeManager) -> None:
        logger.info("Entering STOPPED state on node %s", manager.config.node_id)
        await manager.pg_backend.shutdown()

    async def exit(self, manager: NodeManager) -> None:
        logger.info("Exiting STOPPED state on node %s", manager.config.node_id)

    async def reconcile(self, manager: NodeManager) -> None:
        pass

    def role(self) -> str:
        return "stopped"
