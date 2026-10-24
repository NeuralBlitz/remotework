from __future__ import annotations

from enum import Enum

from .models import Action, GameState, Reward


class AgentState(Enum):
    IDLE = "idle"
    EXPLORING = "exploring"
    ATTACKING = "attacking"
    DEFENDING = "defending"
    FLEEING = "fleeing"


class AgentStateMachine:
    def __init__(self, health_threshold: float = 0.3) -> None:
        self.state = AgentState.IDLE
        self.health_threshold = health_threshold

    def decide(self, game_state: GameState) -> Action:
        if game_state.health_ratio <= self.health_threshold:
            self.state = AgentState.FLEEING
            return Action(action_type="flee", target="", priority=10)
        if game_state.enemies_nearby > 0:
            if game_state.health_ratio > 0.6:
                self.state = AgentState.ATTACKING
                return Action(action_type="attack", target=game_state.nearest_enemy, priority=8)
            else:
                self.state = AgentState.DEFENDING
                return Action(action_type="defend", target="", priority=7)
        if game_state.items_nearby > 0:
            self.state = AgentState.EXPLORING
            return Action(action_type="collect", target="item", priority=5)
        self.state = AgentState.IDLE
        return Action(action_type="idle", target="", priority=0)

    def evaluate_reward(self, action: Action, outcome: str) -> Reward:
        rewards = {"success": 10.0, "partial": 5.0, "failure": -5.0}
        value = rewards.get(outcome, 0.0)
        return Reward(action_type=action.action_type, value=value, outcome=outcome)

