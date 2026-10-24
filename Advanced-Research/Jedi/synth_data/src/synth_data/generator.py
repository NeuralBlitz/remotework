from __future__ import annotations

import hashlib

from synth_data.models import PrivacyMetrics, SyntheticConfig
from synth_data.memento import GeneratorMemento, PrivacyCaretaker


class SyntheticDataGenerator:
    def __init__(self, config: SyntheticConfig) -> None:
        self._config = config
        self._iteration = 0
        self._privacy = PrivacyMetrics()
        self._data: list[list[float]] = []
        self._caretaker = PrivacyCaretaker()
        self._generate()

    def _generate(self) -> None:
        rng_seed = self._config.seed + self._iteration
        self._data = [
            [
                float((rng_seed * (i + j + 1)) % 100) * self._config.noise_level
                for j in range(self._config.num_columns)
            ]
            for i in range(self._config.num_rows)
        ]
        self._privacy.epsilon_used = self._iteration * 0.1
        self._privacy.uniqueness_ratio = max(0.0, 1.0 - self._iteration * 0.1)

    def generate(self) -> list[list[float]]:
        self._iteration += 1
        self._generate()
        return self._data

    def save_state(self) -> GeneratorMemento:
        memento = GeneratorMemento(
            config=SyntheticConfig(
                num_rows=self._config.num_rows,
                num_columns=self._config.num_columns,
                noise_level=self._config.noise_level,
                seed=self._config.seed,
                privacy_epsilon=self._config.privacy_epsilon,
            ),
            privacy=PrivacyMetrics(
                epsilon_used=self._privacy.epsilon_used,
                uniqueness_ratio=self._privacy.uniqueness_ratio,
            ),
            iteration=self._iteration,
            data_hash=hashlib.sha256(str(self._data[:5]).encode()).hexdigest(),
        )
        self._caretaker.save(memento)
        return memento

    def restore_state(self, memento: GeneratorMemento) -> None:
        self._config = SyntheticConfig(
            num_rows=memento.config.num_rows,
            num_columns=memento.config.num_columns,
            noise_level=memento.config.noise_level,
            seed=memento.config.seed,
        )
        self._iteration = memento.iteration
        self._privacy = PrivacyMetrics(
            epsilon_used=memento.privacy.epsilon_used,
            uniqueness_ratio=memento.privacy.uniqueness_ratio,
        )
        self._generate()

    def undo(self) -> bool:
        memento = self._caretaker.undo()
        if memento is None:
            return False
        self.restore_state(memento)
        return True

    def redo(self) -> bool:
        memento = self._caretaker.redo()
        if memento is None:
            return False
        self.restore_state(memento)
        return True

    @property
    def privacy(self) -> PrivacyMetrics:
        return self._privacy

    @property
    def data(self) -> list[list[float]]:
        return self._data

    @property
    def iteration(self) -> int:
        return self._iteration
