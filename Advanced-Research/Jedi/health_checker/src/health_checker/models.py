from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HealthStatus:
    component: str
    healthy: bool
    message: str

    def to_dict(self) -> dict[str, object]:
        return {
            "component": self.component,
            "healthy": self.healthy,
            "message": self.message,
        }
