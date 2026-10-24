from __future__ import annotations

from physics_engine.models import Body
from physics_engine.strategies import AABBCollision, CircleCollision, PhysicsWorld


def test_aabb_collision() -> None:
    strategy = AABBCollision()
    a = Body(body_id="a", position=(0.0, 0.0), width=2.0, height=2.0)
    b = Body(body_id="b", position=(1.5, 0.0), width=2.0, height=2.0)
    collision = strategy.detect(a, b)
    assert collision is not None
    assert collision.overlap_x > 0


def test_aabb_no_collision() -> None:
    strategy = AABBCollision()
    a = Body(body_id="a", position=(0.0, 0.0), width=1.0, height=1.0)
    b = Body(body_id="b", position=(5.0, 5.0), width=1.0, height=1.0)
    assert strategy.detect(a, b) is None


def test_circle_collision() -> None:
    strategy = CircleCollision()
    a = Body(body_id="a", position=(0.0, 0.0), width=2.0, height=2.0)
    b = Body(body_id="b", position=(1.0, 0.0), width=2.0, height=2.0)
    collision = strategy.detect(a, b)
    assert collision is not None


def test_physics_world() -> None:
    world = PhysicsWorld(strategy=AABBCollision())
    world.add_body(Body(body_id="a", position=(0.0, 0.0), width=2.0, height=2.0))
    world.add_body(Body(body_id="b", position=(1.0, 0.0), width=2.0, height=2.0))
    world.add_body(Body(body_id="c", position=(10.0, 10.0), width=1.0, height=1.0))
    collisions = world.step()
    assert len(collisions) == 1
    assert collisions[0].body_a_id == "a"


def test_no_bodies() -> None:
    world = PhysicsWorld()
    assert world.step() == []

