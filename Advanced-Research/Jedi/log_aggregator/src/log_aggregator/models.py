from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LogEntry:
    level: str
    message: str
    timestamp: float

    def to_dict(self) -> dict[str, object]:
        return {
            "level": self.level,
            "message": self.message,
            "timestamp": self.timestamp,
        }
