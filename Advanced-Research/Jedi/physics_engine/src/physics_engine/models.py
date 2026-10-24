from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Body:
    body_id: str
    position: tuple[float, float] = (0.0, 0.0)
    width: float = 1.0
    height: float = 1.0
    mass: float = 1.0
    velocity: tuple[float, float] = (0.0, 0.0)


@dataclass
class Collision:
    body_a_id: str
    body_b_id: str
    overlap_x: float = 0.0
    overlap_y: float = 0.0

