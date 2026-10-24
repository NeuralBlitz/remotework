from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ThreatLevel(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class ThreatAlert:
    level: ThreatLevel = ThreatLevel.NONE
    source: str = ""
    message: str = ""
    input_snippet: str = ""
    timestamp: float = 0.0

    def is_actionable(self, min_level: ThreatLevel = ThreatLevel.MEDIUM) -> bool:
        return self.level.value >= min_level.value

    def __repr__(self) -> str:
        return f"ThreatAlert({self.level.name}: {self.source})"
