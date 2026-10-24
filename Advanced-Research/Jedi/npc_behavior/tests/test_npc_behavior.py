from __future__ import annotations

from npc_behavior.composite import (
    ActionNode,
    ConditionNode,
    InverterNode,
    SelectorNode,
    SequenceNode,
    Status,
)
from npc_behavior.models import NPCState


def test_sequence_success() -> None:
    node = SequenceNode(children=[ActionNode("a"), ActionNode("b")])
    state = NPCState(npc_id="n1")
    assert node.tick(state) == Status.SUCCESS


def test_selector_failure() -> None:
    cond = ConditionNode("is_hostile", value=True)
    state = NPCState(npc_id="n1", is_hostile=False)
    assert cond.tick(state) == Status.FAILURE


def test_selector_picks_first_success() -> None:
    node = SelectorNode(children=[
        ConditionNode("is_hostile", value=True),
        ActionNode("wander"),
    ])
    state = NPCState(npc_id="n1")
    result = node.tick(state)
    assert result == Status.SUCCESS
    assert state.last_action == "wander"


def test_inverter() -> None:
    node = InverterNode(ConditionNode("is_hostile", value=False))
    state = NPCState(npc_id="n1", is_hostile=False)
    assert node.tick(state) == Status.FAILURE


def test_complex_tree() -> None:
    tree = SelectorNode(children=[
        SequenceNode(children=[
            ConditionNode("is_hostile", value=True),
            ConditionNode("has_target", value=True),
            ActionNode("attack"),
        ]),
        ActionNode("idle"),
    ])
    state = NPCState(npc_id="n1", is_hostile=True, has_target=True)
    result = tree.tick(state)
    assert result == Status.SUCCESS
    assert state.last_action == "attack"

