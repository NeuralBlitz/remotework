from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CircuitState:
    name: str
    failures: int
    threshold: int

    def is_open(self) -> bool:
        return self.failures >= self.threshold
