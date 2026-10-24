from __future__ import annotations

from pg_temporal.memento import Caretaker, Originator
from pg_temporal.models import LSNPosition, Memento


class TemporalManager:
    def __init__(self) -> None:
        self._originator = Originator()
        self._caretaker = Caretaker()

    def set(self, key: str, value: object) -> None:
        self._originator.set(key, value)

    def get(self, key: str) -> object | None:
        return self._originator.get(key)

    def snapshot(self, label: str = "") -> Memento:
        memento = self._originator.save(label)
        self._caretaker.save(memento)
        return memento

    def rewind_to_lsn(self, lsn: LSNPosition) -> Memento | None:
        memento = self._caretaker.get_at_lsn(lsn)
        if memento is not None:
            self._originator.restore(memento)
        return memento

    def rewind_to_label(self, label: str) -> Memento | None:
        memento = self._caretaker.get_by_label(label)
        if memento is not None:
            self._originator.restore(memento)
        return memento

    @property
    def lsn(self) -> LSNPosition:
        return self._originator.lsn

    @property
    def state(self) -> dict[str, object]:
        return self._originator.state

    @property
    def history(self) -> list[Memento]:
        return self._caretaker.history
