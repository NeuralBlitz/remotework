from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class CodePhase(Enum):
    DRAFTING = auto()
    TESTING = auto()
    REFACTORING = auto()
    FINALIZING = auto()


@dataclass
class CodeArtifact:
    source: str = ""
    tests: str = ""
    errors: list[str] = field(default_factory=list)
    refactors_applied: int = 0

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0 and bool(self.source.strip())
