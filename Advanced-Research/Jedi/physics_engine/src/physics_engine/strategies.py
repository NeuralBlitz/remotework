from __future__ import annotations

import math
from abc import ABC, abstractmethod

from .models import Body, Collision


class CollisionStrategy(ABC):
    @abstractmethod
    def detect(self, body_a: Body, body_b: Body) -> Collision | None:
        raise NotImplementedError


class AABBCollision(CollisionStrategy):
    def detect(self, body_a: Body, body_b: Body) -> Collision | None:
        ax, ay = body_a.position
        bx, by = body_b.position
        overlap_x = (body_a.width + body_b.width) / 2 - abs(ax - bx)
        overlap_y = (body_a.height + body_b.height) / 2 - abs(ay - by)
        if overlap_x > 0 and overlap_y > 0:
            return Collision(
                body_a_id=body_a.body_id,
                body_b_id=body_b.body_id,
                overlap_x=overlap_x,
                overlap_y=overlap_y,
            )
        return None


class CircleCollision(CollisionStrategy):
    def detect(self, body_a: Body, body_b: Body) -> Collision | None:
        ax, ay = body_a.position
        bx, by = body_b.position
        dist = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
        radius_a = min(body_a.width, body_a.height) / 2
        radius_b = min(body_b.width, body_b.height) / 2
        if dist < radius_a + radius_b:
            return Collision(
                body_a_id=body_a.body_id,
                body_b_id=body_b.body_id,
                overlap_x=radius_a + radius_b - dist,
                overlap_y=0.0,
            )
        return None


class PhysicsWorld:
    def __init__(self, strategy: CollisionStrategy | None = None) -> None:
        self.strategy = strategy or AABBCollision()
        self.bodies: list[Body] = []

    def add_body(self, body: Body) -> None:
        self.bodies.append(body)

    def step(self) -> list[Collision]:
        collisions: list[Collision] = []
        for i, a in enumerate(self.bodies):
            for b in self.bodies[i + 1 :]:
                collision = self.strategy.detect(a, b)
                if collision:
                    collisions.append(collision)
        return collisions

