from __future__ import annotations

from pg_devicetwin.models import DeviceMemento, DeviceState


class DeviceTwin:
    def __init__(self, state: DeviceState) -> None:
        self._state = state

    @property
    def state(self) -> DeviceState:
        return self._state

    def save(self) -> DeviceMemento:
        return self._state.snapshot()

    def restore(self, memento: DeviceMemento) -> None:
        self._state = memento.restore()

    def update_telemetry(self, key: str, value: object) -> None:
        self._state.telemetry[key] = value

    def update_config(self, key: str, value: object) -> None:
        self._state.config[key] = value

    def increment_errors(self) -> None:
        self._state.error_count += 1


class StateHistory:
    def __init__(self, max_size: int = 100) -> None:
        self._history: list[DeviceMemento] = []
        self._max_size = max_size

    def push(self, memento: DeviceMemento) -> None:
        self._history.append(memento)
        if len(self._history) > self._max_size:
            self._history.pop(0)

    def pop(self) -> DeviceMemento | None:
        if not self._history:
            return None
        return self._history.pop()

    def peek(self) -> DeviceMemento | None:
        if not self._history:
            return None
        return self._history[-1]

    def list_snapshots(self) -> list[DeviceMemento]:
        return list(self._history)

    @property
    def size(self) -> int:
        return len(self._history)

    def clear(self) -> None:
        self._history.clear()
