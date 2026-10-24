from datetime import datetime

import pytest

from pg_tuesday.models import MaintenanceState, MaintenanceWindow, PatchResult
from pg_tuesday.orchestrator import MaintenanceOrchestrator
from pg_tuesday.states import InvalidTransitionError, MaintenanceStateMachine


class MockPatcher:
    def __init__(self, fail_verify: bool = False) -> None:
        self.fail_verify = fail_verify

    def drain(self, node_id: str) -> bool:
        return True

    def apply_patch(self, node_id: str) -> PatchResult:
        return PatchResult(
            node_id=node_id,
            success=True,
            pre_patch_version="14.0",
            post_patch_version="14.1",
            duration_seconds=5.0,
        )

    def verify(self, node_id: str) -> bool:
        return not self.fail_verify


def _make_window(nodes: list[str] | None = None) -> MaintenanceWindow:
    return MaintenanceWindow(
        scheduled_at=datetime(2026, 3, 10, 2, 0),
        node_ids=nodes or ["node-1", "node-2"],
    )


class TestMaintenanceStateEnum:
    def test_states_exist(self) -> None:
        assert MaintenanceState.SCHEDULED.value == "scheduled"
        assert MaintenanceState.COMPLETED.value == "completed"
        assert MaintenanceState.FAILED.value == "failed"


class TestMaintenanceStateMachine:
    def test_initial_state(self) -> None:
        window = _make_window()
        sm = MaintenanceStateMachine(window)
        assert sm.current_state == MaintenanceState.SCHEDULED

    def test_valid_transitions(self) -> None:
        window = _make_window()
        sm = MaintenanceStateMachine(window)
        sm.transition(MaintenanceState.DRAINING_TRAFFIC)
        assert sm.current_state == MaintenanceState.DRAINING_TRAFFIC
        sm.transition(MaintenanceState.PATCHING)
        assert sm.current_state == MaintenanceState.PATCHING

    def test_invalid_transition_raises(self) -> None:
        window = _make_window()
        sm = MaintenanceStateMachine(window)
        with pytest.raises(InvalidTransitionError):
            sm.transition(MaintenanceState.PATCHING)

    def test_allowed_transitions(self) -> None:
        window = _make_window()
        sm = MaintenanceStateMachine(window)
        allowed = sm.allowed_transitions()
        assert MaintenanceState.DRAINING_TRAFFIC in allowed
        assert MaintenanceState.PATCHING not in allowed

    def test_guard_drain_requires_scheduled(self) -> None:
        window = _make_window()
        sm = MaintenanceStateMachine(window)
        assert sm.guard_drain(0) is True
        assert sm.guard_drain(5) is False

    def test_guard_complete_requires_all_patched(self) -> None:
        window = _make_window(["node-1"])
        window.state = MaintenanceState.VERIFYING
        window.patch_results = [
            PatchResult("node-1", True, "14.0", "14.1", 3.0),
        ]
        sm = MaintenanceStateMachine(window)
        assert sm.guard_complete() is True

    def test_guard_complete_fails_if_missing(self) -> None:
        window = _make_window(["node-1", "node-2"])
        window.state = MaintenanceState.VERIFYING
        window.patch_results = [PatchResult("node-1", True, "14.0", "14.1", 3.0)]
        sm = MaintenanceStateMachine(window)
        assert sm.guard_complete() is False


class TestMaintenanceOrchestrator:
    def test_full_workflow_success(self) -> None:
        window = _make_window(["node-1"])
        orch = MaintenanceOrchestrator(window, MockPatcher())
        state = orch.run_full_workflow(active_connections=0)
        assert state == MaintenanceState.COMPLETED
        assert window.completed_at is not None

    def test_drain_with_active_connections_raises(self) -> None:
        window = _make_window()
        orch = MaintenanceOrchestrator(window, MockPatcher())
        with pytest.raises(RuntimeError):
            orch.drain_traffic(active_connections=10)

    def test_verify_failure_transitions_to_failed(self) -> None:
        window = _make_window(["node-1"])
        orch = MaintenanceOrchestrator(window, MockPatcher(fail_verify=True))
        orch.drain_traffic(0)
        orch.apply_patches()
        state = orch.verify_and_complete()
        assert state == MaintenanceState.FAILED

    def test_patch_results_collected(self) -> None:
        window = _make_window(["a", "b", "c"])
        orch = MaintenanceOrchestrator(window, MockPatcher())
        orch.drain_traffic(0)
        orch.apply_patches()
        assert len(window.patch_results) == 3

    def test_cannot_patch_before_drain(self) -> None:
        window = _make_window()
        orch = MaintenanceOrchestrator(window, MockPatcher())
        with pytest.raises(RuntimeError):
            orch.apply_patches()

    def test_window_all_nodes_patched(self) -> None:
        window = _make_window(["n1"])
        window.patch_results = [PatchResult("n1", True, "14.0", "14.1", 1.0)]
        assert window.all_nodes_patched() is True
        assert window.has_failures() is False

    def test_window_has_failures(self) -> None:
        window = _make_window(["n1", "n2"])
        window.patch_results = [
            PatchResult("n1", True, "14.0", "14.1", 1.0),
            PatchResult("n2", False, "14.0", "14.0", 2.0, error_message="timeout"),
        ]
        assert window.all_nodes_patched() is False
        assert window.has_failures() is True

    def test_started_at_set_on_drain(self) -> None:
        window = _make_window()
        orch = MaintenanceOrchestrator(window, MockPatcher())
        assert window.started_at is None
        orch.drain_traffic(0)
        assert window.started_at is not None
