from __future__ import annotations

from game_ai.models import Action, GameState
from game_ai.states import AgentState, AgentStateMachine


def test_idle_state() -> None:
    sm = AgentStateMachine()
    action = sm.decide(GameState())
    assert action.action_type == "idle"
    assert sm.state == AgentState.IDLE


def test_attack_state() -> None:
    sm = AgentStateMachine()
    state = GameState(health_ratio=0.8, enemies_nearby=1, nearest_enemy="goblin")
    action = sm.decide(state)
    assert action.action_type == "attack"
    assert sm.state == AgentState.ATTACKING


def test_flee_state() -> None:
    sm = AgentStateMachine()
    state = GameState(health_ratio=0.1, enemies_nearby=2)
    action = sm.decide(state)
    assert action.action_type == "flee"
    assert sm.state == AgentState.FLEEING


def test_defend_state() -> None:
    sm = AgentStateMachine()
    state = GameState(health_ratio=0.5, enemies_nearby=1)
    action = sm.decide(state)
    assert action.action_type == "defend"


def test_reward_evaluation() -> None:
    sm = AgentStateMachine()
    action = Action(action_type="attack")
    reward = sm.evaluate_reward(action, "success")
    assert reward.value == 10.0

