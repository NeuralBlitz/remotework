from __future__ import annotations

from datetime import datetime

import pytest

from pg_contagg.models import AggregateState, RefreshConfig
from pg_contagg.refresher import AggregateRefresher, RefreshResult
from pg_contagg.states import AggregateStateMachine


@pytest.fixture
def config() -> RefreshConfig:
    return RefreshConfig(
        view_name="hourly_metrics",
        source_table="metrics",
        refresh_interval="1 hour",
    )


@pytest.fixture
def machine(config: RefreshConfig) -> AggregateStateMachine:
    return AggregateStateMachine(config)


@pytest.fixture
def refresher() -> AggregateRefresher:
    return AggregateRefresher()


class TestRefreshConfig:
    def test_validate_valid(self, config: RefreshConfig) -> None:
        assert config.validate() is True

    def test_validate_invalid(self) -> None:
        assert RefreshConfig(view_name="", source_table="").validate() is False


class TestAggregateStateMachine:
    def test_initial_state(self, machine: AggregateStateMachine) -> None:
        assert machine.state == AggregateState.STALE

    def test_start_refresh(self, machine: AggregateStateMachine) -> None:
        assert machine.start_refresh(datetime.now()) is True
        assert machine.state == AggregateState.REFRESHING

    def test_start_refresh_while_refreshing_raises(self, machine: AggregateStateMachine) -> None:
        machine.start_refresh(datetime.now())
        with pytest.raises(RuntimeError, match="already in progress"):
            machine.start_refresh(datetime.now())

    def test_complete_refresh(self, machine: AggregateStateMachine) -> None:
        now = datetime(2024, 6, 1)
        machine.start_refresh(now)
        assert machine.complete_refresh(now) is True
        assert machine.state == AggregateState.CURRENT
        assert machine.refresh_count == 1
        assert machine.last_refresh == now

    def test_complete_without_start_raises(self, machine: AggregateStateMachine) -> None:
        with pytest.raises(RuntimeError, match="No refresh in progress"):
            machine.complete_refresh(datetime.now())

    def test_fail_refresh(self, machine: AggregateStateMachine) -> None:
        machine.start_refresh(datetime.now())
        assert machine.fail_refresh("timeout") is True
        assert machine.state == AggregateState.ERROR
        assert machine.error_message == "timeout"

    def test_mark_stale(self, machine: AggregateStateMachine) -> None:
        machine.start_refresh(datetime.now())
        machine.complete_refresh(datetime.now())
        assert machine.mark_stale() is True
        assert machine.state == AggregateState.STALE

    def test_mark_stale_while_refreshing_raises(self, machine: AggregateStateMachine) -> None:
        machine.start_refresh(datetime.now())
        with pytest.raises(RuntimeError, match="Cannot mark stale"):
            machine.mark_stale()

    def test_can_refresh_states(self, machine: AggregateStateMachine) -> None:
        assert machine.can_refresh() is True
        machine.start_refresh(datetime.now())
        assert machine.can_refresh() is False

    def test_reset(self, machine: AggregateStateMachine) -> None:
        machine.start_refresh(datetime.now())
        machine.complete_refresh(datetime.now())
        machine.reset()
        assert machine.state == AggregateState.STALE
        assert machine.refresh_count == 0

    def test_listener_called(self, config: RefreshConfig) -> None:
        transitions: list[tuple[AggregateState, AggregateState]] = []
        machine = AggregateStateMachine(config)
        machine.add_listener(lambda o, n: transitions.append((o, n)))
        machine.start_refresh(datetime.now())
        machine.complete_refresh(datetime.now())
        assert len(transitions) == 2

    def test_invalid_config_raises(self) -> None:
        with pytest.raises(ValueError):
            AggregateStateMachine(RefreshConfig(view_name="", source_table=""))


class TestAggregateRefresher:
    def test_register(self, refresher: AggregateRefresher, config: RefreshConfig) -> None:
        machine = refresher.register(config)
        assert isinstance(machine, AggregateStateMachine)
        assert "hourly_metrics" in refresher.list_views()

    def test_register_duplicate_raises(
        self, refresher: AggregateRefresher, config: RefreshConfig
    ) -> None:
        refresher.register(config)
        with pytest.raises(ValueError, match="Already registered"):
            refresher.register(config)

    def test_unregister(self, refresher: AggregateRefresher, config: RefreshConfig) -> None:
        refresher.register(config)
        refresher.unregister("hourly_metrics")
        assert "hourly_metrics" not in refresher.list_views()

    def test_unregister_missing_raises(self, refresher: AggregateRefresher) -> None:
        with pytest.raises(KeyError):
            refresher.unregister("missing")

    def test_refresh(self, refresher: AggregateRefresher, config: RefreshConfig) -> None:
        refresher.register(config)
        now = datetime(2024, 6, 1)
        result = refresher.refresh("hourly_metrics", now)
        assert result.success is True
        assert result.state == AggregateState.CURRENT
        assert refresher.get_state("hourly_metrics") == AggregateState.CURRENT

    def test_refresh_missing_raises(self, refresher: AggregateRefresher) -> None:
        with pytest.raises(KeyError):
            refresher.refresh("nope")

    def test_mark_all_stale(self, refresher: AggregateRefresher) -> None:
        c1 = RefreshConfig("v1", "t1")
        c2 = RefreshConfig("v2", "t2")
        refresher.register(c1)
        refresher.register(c2)
        now = datetime.now()
        refresher.refresh("v1", now)
        refresher.refresh("v2", now)
        assert refresher.mark_all_stale() == 2

    def test_refresh_all(self, refresher: AggregateRefresher) -> None:
        refresher.register(RefreshConfig("v1", "t1"))
        refresher.register(RefreshConfig("v2", "t2"))
        results = refresher.refresh_all(datetime.now())
        assert len(results) == 2
        assert all(r.success for r in results)

    def test_get_stale_views(self, refresher: AggregateRefresher) -> None:
        refresher.register(RefreshConfig("v1", "t1"))
        refresher.register(RefreshConfig("v2", "t2"))
        refresher.refresh("v1", datetime.now())
        stale = refresher.get_stale_views()
        assert "v1" not in stale
        assert "v2" in stale
