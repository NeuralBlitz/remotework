import pytest
from pg_cloudfailover.manager import FailoverManager
from pg_cloudfailover.models import FailoverState
from pg_cloudfailover.states import FailoverStateMachine


def test_initial_state_is_primary() -> None:
    sm = FailoverStateMachine()
    assert sm.state == FailoverState.PRIMARY


def test_full_failover_cycle() -> None:
    sm = FailoverStateMachine()
    sm.initiate_failover()
    assert sm.state == FailoverState.FAILING_OVER
    sm.promote_standby()
    assert sm.state == FailoverState.STANDBY_PROMOTED
    sm.start_rebuild()
    assert sm.state == FailoverState.REBUILDING
    sm.complete_rebuild()
    assert sm.state == FailoverState.PRIMARY


def test_invalid_transition_raises() -> None:
    sm = FailoverStateMachine()
    with pytest.raises(ValueError):
        sm.promote_standby()


def test_can_transition() -> None:
    sm = FailoverStateMachine()
    assert sm.can_transition(FailoverState.FAILING_OVER)
    assert not sm.can_transition(FailoverState.REBUILDING)


def test_manager_registers_cluster() -> None:
    mgr = FailoverManager()
    mgr.register_cluster("prod")
    assert "prod" in mgr.list_clusters()


def test_manager_executes_failover() -> None:
    mgr = FailoverManager()
    mgr.register_cluster("prod")
    events = mgr.execute_failover("prod")
    assert len(events) == 5
    assert mgr.get_cluster("prod").state == FailoverState.PRIMARY


def test_manager_duplicate_cluster_raises() -> None:
    mgr = FailoverManager()
    mgr.register_cluster("prod")
    with pytest.raises(ValueError):
        mgr.register_cluster("prod")


def test_history_records_all_events() -> None:
    sm = FailoverStateMachine()
    sm.initiate_failover()
    sm.promote_standby()
    assert len(sm.history) == 3
