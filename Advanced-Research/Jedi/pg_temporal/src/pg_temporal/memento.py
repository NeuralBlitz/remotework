from __future__ import annotations

from pg_temporal.models import LSNPosition, Memento


class Originator:
    def __init__(self) -> None:
        self._state: dict[str, object] = {}
        self._lsn = LSNPosition(0, 0)

    def set(self, key: str, value: object) -> None:
        self._state[key] = value
        self._lsn = LSNPosition(self._lsn.segment, self._lsn.offset + 1)

    def get(self, key: str) -> object | None:
        return self._state.get(key)

    def save(self, label: str = "") -> Memento:
        return Memento(
            lsn=LSNPosition(self._lsn.segment, self._lsn.offset),
            state=dict(self._state),
            label=label,
        )

    def restore(self, memento: Memento) -> None:
        self._state = dict(memento.state)
        self._lsn = memento.lsn

    @property
    def lsn(self) -> LSNPosition:
        return self._lsn

    @property
    def state(self) -> dict[str, object]:
        return dict(self._state)


class Caretaker:
    def __init__(self) -> None:
        self._history: list[Memento] = []

    def save(self, memento: Memento) -> None:
        self._history.append(memento)

    def get_at_lsn(self, lsn: LSNPosition) -> Memento | None:
        for m in reversed(self._history):
            if m.lsn <= lsn:
                return m
        return None

    def get_by_label(self, label: str) -> Memento | None:
        for m in reversed(self._history):
            if m.label == label:
                return m
        return None

    @property
    def history(self) -> list[Memento]:
        return list(self._history)

    def clear(self) -> None:
        self._history.clear()
