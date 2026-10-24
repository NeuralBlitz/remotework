from __future__ import annotations

from dataclasses import dataclass, field

from synth_data.models import PrivacyMetrics, SyntheticConfig


@dataclass
class GeneratorMemento:
    config: SyntheticConfig
    privacy: PrivacyMetrics
    iteration: int
    data_hash: str

    def __repr__(self) -> str:
        return f"GeneratorMemento(iter={self.iteration}, hash={self.data_hash[:8]})"


class PrivacyCaretaker:
    def __init__(self) -> None:
        self._history: list[GeneratorMemento] = []
        self._current_index: int = -1

    def save(self, memento: GeneratorMemento) -> None:
        self._history = self._history[: self._current_index + 1]
        self._history.append(memento)
        self._current_index += 1

    def undo(self) -> GeneratorMemento | None:
        if self._current_index <= 0:
            return None
        self._current_index -= 1
        return self._history[self._current_index]

    def redo(self) -> GeneratorMemento | None:
        if self._current_index >= len(self._history) - 1:
            return None
        self._current_index += 1
        return self._history[self._current_index]

    def current(self) -> GeneratorMemento | None:
        if 0 <= self._current_index < len(self._history):
            return self._history[self._current_index]
        return None

    def history_size(self) -> int:
        return len(self._history)

    def can_undo(self) -> bool:
        return self._current_index > 0

    def can_redo(self) -> bool:
        return self._current_index < len(self._history) - 1
