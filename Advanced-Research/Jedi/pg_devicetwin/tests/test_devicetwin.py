
import pytest

from pg_devicetwin.memento import DeviceTwin, StateHistory
from pg_devicetwin.models import DeviceMemento, DeviceState, DeviceStatus


def _make_state(**overrides: object) -> DeviceState:
    defaults: dict[str, object] = {
        "device_id": "sensor-001",
        "status": DeviceStatus.ONLINE,
        "firmware_version": "1.0.0",
        "telemetry": {"temperature": 22.5},
        "config": {"interval": 60},
    }
    defaults.update(overrides)
    return DeviceState(**defaults)


class TestDeviceState:
    def test_create_state(self) -> None:
        state = _make_state()
        assert state.device_id == "sensor-001"
        assert state.status == DeviceStatus.ONLINE

    def test_snapshot_creates_memento(self) -> None:
        state = _make_state()
        memento = state.snapshot()
        assert isinstance(memento, DeviceMemento)
        assert memento.device_id == state.device_id
        assert memento.status == state.status


class TestDeviceMemento:
    def test_restore_from_memento(self) -> None:
        state = _make_state()
        memento = state.snapshot()
        restored = memento.restore()
        assert restored.device_id == state.device_id
        assert restored.firmware_version == state.firmware_version
        assert restored.telemetry == state.telemetry

    def test_memento_is_frozen(self) -> None:
        state = _make_state()
        memento = state.snapshot()
        with pytest.raises(AttributeError):
            memento.device_id = "changed"  # type: ignore[misc]

    def test_restore_deep_copies_telemetry(self) -> None:
        state = _make_state(telemetry={"temp": 20})
        memento = state.snapshot()
        state.telemetry["temp"] = 99
        restored = memento.restore()
        assert restored.telemetry["temp"] == 20


class TestDeviceTwin:
    def test_save_and_restore(self) -> None:
        state = _make_state()
        twin = DeviceTwin(state)
        memento = twin.save()
        twin.update_telemetry("temperature", 99.0)
        assert twin.state.telemetry["temperature"] == 99.0
        twin.restore(memento)
        assert twin.state.telemetry["temperature"] == 22.5

    def test_update_config(self) -> None:
        twin = DeviceTwin(_make_state())
        twin.update_config("timeout", 30)
        assert twin.state.config["timeout"] == 30

    def test_increment_errors(self) -> None:
        twin = DeviceTwin(_make_state())
        assert twin.state.error_count == 0
        twin.increment_errors()
        twin.increment_errors()
        assert twin.state.error_count == 2


class TestStateHistory:
    def test_push_and_pop(self) -> None:
        history = StateHistory()
        state = _make_state()
        memento = state.snapshot()
        history.push(memento)
        assert history.size == 1
        popped = history.pop()
        assert popped is not None
        assert popped.device_id == state.device_id
        assert history.size == 0

    def test_pop_empty_returns_none(self) -> None:
        history = StateHistory()
        assert history.pop() is None

    def test_peek(self) -> None:
        history = StateHistory()
        state = _make_state()
        memento = state.snapshot()
        history.push(memento)
        peeked = history.peek()
        assert peeked is not None
        assert history.size == 1

    def test_max_size_eviction(self) -> None:
        history = StateHistory(max_size=2)
        for i in range(3):
            history.push(_make_state(device_id=f"dev-{i}").snapshot())
        assert history.size == 2
        snapshots = history.list_snapshots()
        assert snapshots[0].device_id == "dev-1"

    def test_clear(self) -> None:
        history = StateHistory()
        history.push(_make_state().snapshot())
        history.clear()
        assert history.size == 0

    def test_list_snapshots(self) -> None:
        history = StateHistory()
        for i in range(3):
            history.push(_make_state(device_id=f"dev-{i}").snapshot())
        snaps = history.list_snapshots()
        assert len(snaps) == 3
