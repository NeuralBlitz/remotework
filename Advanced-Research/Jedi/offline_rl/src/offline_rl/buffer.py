from __future__ import annotations

from offline_rl.models import Trajectory, Transition
from offline_rl.prototype import TrajectoryPrototype


class ReplayBuffer:
    def __init__(self, capacity: int = 10000) -> None:
        self._capacity = capacity
        self._trajectories: list[Trajectory] = []
        self._transitions: list[Transition] = []

    def add_trajectory(self, trajectory: Trajectory) -> None:
        self._trajectories.append(trajectory)
        self._transitions.extend(trajectory.transitions)
        self._trim()

    def add_from_prototype(self, prototype: TrajectoryPrototype, **kwargs: object) -> Trajectory:
        if "scale" in kwargs:
            traj = prototype.mutate_rewards(float(kwargs["scale"]))
        else:
            traj = prototype.clone()
        self.add_trajectory(traj)
        return traj

    def sample_trajectories(self, n: int) -> list[Trajectory]:
        import random
        return random.sample(self._trajectories, min(n, len(self._trajectories)))

    def sample_transitions(self, n: int) -> list[Transition]:
        import random
        return random.sample(self._transitions, min(n, len(self._transitions)))

    def _trim(self) -> None:
        while len(self._transitions) > self._capacity and self._transitions:
            self._transitions.pop(0)
        while len(self._trajectories) > self._capacity // 10 and self._trajectories:
            self._trajectories.pop(0)

    def trajectory_count(self) -> int:
        return len(self._trajectories)

    def transition_count(self) -> int:
        return len(self._transitions)

    def clear(self) -> None:
        self._trajectories.clear()
        self._transitions.clear()

    def total_reward(self) -> float:
        return sum(t.total_reward for t in self._trajectories)
