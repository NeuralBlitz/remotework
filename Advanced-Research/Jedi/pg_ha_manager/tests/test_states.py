"""Tests for the State Pattern implementation."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from pg_ha_manager.backends import ElectionClient, HealthResult, PgBackend
from pg_ha_manager.models import ClusterConfig, NodeStatus
from pg_ha_manager.node import NodeManager
from pg_ha_manager.states import Candidate, Follower, Leader, Stopped


@pytest.fixture
def config() -> ClusterConfig:
    return ClusterConfig(
        node_id="test-node-1",
        postgres_host="localhost",
        postgres_port=5432,
        etcd_endpoints=["http://localhost:2379"],
        health_check_interval=1.0,
        max_consecutive_failures=3,
    )


@pytest.fixture
def healthy_backend() -> PgBackend:
    backend = MagicMock(spec=PgBackend)
    backend.check_health = AsyncMock(
        return_value=HealthResult(
            status=NodeStatus.HEALTHY,
            is_postgres_running=True,
            replication_lag_bytes=0,
            consecutive_failures=0,
        )
    )
    backend.initialize = AsyncMock()
    backend.promote = AsyncMock()
    backend.follow = AsyncMock()
    backend.stop_accepting_writes = AsyncMock()
    backend.shutdown = AsyncMock()
    backend.update_config = AsyncMock()
    return backend


@pytest.fixture
def election_client() -> ElectionClient:
    client = MagicMock(spec=ElectionClient)
    client.connect = AsyncMock()
    client.disconnect = AsyncMock()
    client.acquire_lease = AsyncMock(return_value=True)
    client.release_lease = AsyncMock()
    client.renew_lease = AsyncMock(return_value=True)
    client.try_acquire_lease = AsyncMock(return_value=True)
    client.is_leader_alive = AsyncMock(return_value=True)
    client.get_current_leader = AsyncMock(return_value="test-node-1")
    return client


class TestStateTransitions:
    """Test state transition logic."""

    @pytest.mark.asyncio
    async def test_start_enters_follower(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        manager = NodeManager(config, healthy_backend, election_client)
        await manager.start()
        assert manager.role == "follower" or manager.role == "leader"
        await manager.stop()

    @pytest.mark.asyncio
    async def test_candidate_wins_becomes_leader(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        election_client.try_acquire_lease = AsyncMock(return_value=True)
        manager = NodeManager(config, healthy_backend, election_client)
        await manager.transition_to(Candidate())
        await manager.reconcile()
        assert manager.role == "leader"

    @pytest.mark.asyncio
    async def test_candidate_loses_becomes_follower(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        election_client.try_acquire_lease = AsyncMock(return_value=False)
        election_client.get_current_leader = AsyncMock(return_value="other-node")
        manager = NodeManager(config, healthy_backend, election_client)
        await manager.transition_to(Candidate())
        await manager.reconcile()
        assert manager.role == "follower"

    @pytest.mark.asyncio
    async def test_leader_demotes_when_unhealthy(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        healthy_backend.check_health = AsyncMock(
            return_value=HealthResult(
                status=NodeStatus.UNREACHABLE,
                is_postgres_running=False,
                replication_lag_bytes=0,
                consecutive_failures=3,
            )
        )
        manager = NodeManager(config, healthy_backend, election_client)
        await manager.transition_to(Leader())
        await manager.reconcile()
        assert manager.role == "candidate"

    @pytest.mark.asyncio
    async def test_follower_promotes_when_leader_dead(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        election_client.is_leader_alive = AsyncMock(return_value=False)
        manager = NodeManager(config, healthy_backend, election_client)
        await manager.transition_to(Follower())
        await manager.reconcile()
        assert manager.role == "candidate"

    @pytest.mark.asyncio
    async def test_no_op_same_state_transition(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        manager = NodeManager(config, healthy_backend, election_client)
        await manager.transition_to(Stopped())
        # Transitioning to same state should be a no-op
        await manager.transition_to(Stopped())
        assert manager.role == "stopped"


class TestLeaderState:
    """Test Leader state behavior."""

    @pytest.mark.asyncio
    async def test_leader_enters_correctly(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        manager = NodeManager(config, healthy_backend, election_client)
        state = Leader()
        await state.enter(manager)
        healthy_backend.promote.assert_called_once()
        election_client.acquire_lease.assert_called_once()

    @pytest.mark.asyncio
    async def test_leader_exits_correctly(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        manager = NodeManager(config, healthy_backend, election_client)
        state = Leader()
        await state.exit(manager)
        election_client.release_lease.assert_called_once()

    @pytest.mark.asyncio
    async def test_leader_renews_lease(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        manager = NodeManager(config, healthy_backend, election_client)
        state = Leader()
        await state.reconcile(manager)
        election_client.renew_lease.assert_called_once()


class TestFollowerState:
    """Test Follower state behavior."""

    @pytest.mark.asyncio
    async def test_follower_enters_correctly(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        manager = NodeManager(config, healthy_backend, election_client)
        state = Follower()
        await state.enter(manager)
        healthy_backend.follow.assert_called_once()


class TestCandidateState:
    """Test Candidate state behavior."""

    @pytest.mark.asyncio
    async def test_candidate_stops_writes_on_enter(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        manager = NodeManager(config, healthy_backend, election_client)
        state = Candidate()
        await state.enter(manager)
        healthy_backend.stop_accepting_writes.assert_called_once()


class TestNodeInfo:
    """Test NodeInfo retrieval."""

    @pytest.mark.asyncio
    async def test_get_node_info(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        manager = NodeManager(config, healthy_backend, election_client)
        await manager.transition_to(Follower())
        info = await manager.get_node_info()
        assert info.node_id == "test-node-1"
        assert info.role == "follower"
        assert info.is_postgres_running is True


class TestTransitionCallbacks:
    """Test transition callback system."""

    @pytest.mark.asyncio
    async def test_callback_called_on_transition(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        manager = NodeManager(config, healthy_backend, election_client)
        transitions: list[tuple[str, str]] = []
        manager.on_transition(lambda old, new: transitions.append((old, new)))

        await manager.transition_to(Leader())
        assert len(transitions) == 1
        assert transitions[0] == ("stopped", "leader")

    @pytest.mark.asyncio
    async def test_callback_error_does_not_crash(
        self, config: ClusterConfig, healthy_backend: PgBackend, election_client: ElectionClient
    ) -> None:
        manager = NodeManager(config, healthy_backend, election_client)
        manager.on_transition(lambda old, new: (_ for _ in ()).throw(RuntimeError("boom")))
        # Should not raise
        await manager.transition_to(Leader())
        assert manager.role == "leader"
