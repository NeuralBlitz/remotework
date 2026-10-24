from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GameState:
    health_ratio: float = 1.0
    enemies_nearby: int = 0
    items_nearby: int = 0
    nearest_enemy: str = ""
    position: tuple[float, float] = (0.0, 0.0)


@dataclass
class Action:
    action_type: str = "idle"
    target: str = ""
    priority: int = 0


@dataclass
class Reward:
    action_type: str = ""
    value: float = 0.0
    outcome: str = ""

