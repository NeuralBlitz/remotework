from __future__ import annotations

import copy

from offline_rl.models import Trajectory, Transition


class TrajectoryPrototype:
    def __init__(self, trajectory: Trajectory) -> None:
        self._template = trajectory

    def clone(self, new_id: str = "") -> Trajectory:
        cloned = Trajectory(
            transitions=[copy.deepcopy(t) for t in self._template.transitions],
            episode_id=new_id or f"{self._template.episode_id}_clone",
            total_reward=self._template.total_reward,
        )
        return cloned

    def mutate_rewards(self, scale: float, offset: float = 0.0) -> Trajectory:
        mutated = self.clone()
        for t in mutated.transitions:
            t.reward = t.reward * scale + offset
        mutated.total_reward = mutated.compute_return()
        return mutated

    def truncate(self, length: int) -> Trajectory:
        if length <= 0:
            return Trajectory(episode_id=f"{self._template.episode_id}_trunc")
        truncated = Trajectory(
            transitions=self._template.transitions[:length],
            episode_id=f"{self._template.episode_id}_trunc",
        )
        if truncated.transitions:
            truncated.transitions[-1].done = True
        truncated.total_reward = truncated.compute_return()
        return truncated

    @property
    def template(self) -> Trajectory:
        return self._template


class HindsightPrototype(TrajectoryPrototype):
    def __init__(self, trajectory: Trajectory) -> None:
        super().__init__(trajectory)

    def relabel_goals(self, new_goal: list[float]) -> Trajectory:
        relabeled = self.clone()
        for t in relabeled.transitions:
            t.next_state = list(new_goal)
        return relabeled

    def relabel_rewards(self, goal: list[float], threshold: float = 0.1) -> Trajectory:
        relabeled = self.clone()
        for t in relabeled.transitions:
            dist = sum((s - g) ** 2 for s, g in zip(t.next_state, goal)) ** 0.5
            t.reward = 1.0 if dist < threshold else 0.0
        relabeled.total_reward = relabeled.compute_return()
        return relabeled
