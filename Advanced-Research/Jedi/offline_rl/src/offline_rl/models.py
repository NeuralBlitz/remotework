from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Transition:
    state: list[float] = field(default_factory=list)
    action: list[float] = field(default_factory=list)
    reward: float = 0.0
    next_state: list[float] = field(default_factory=list)
    done: bool = False

    def is_terminal(self) -> bool:
        return self.done


@dataclass
class Trajectory:
    transitions: list[Transition] = field(default_factory=list)
    episode_id: str = ""
    total_reward: float = 0.0

    def length(self) -> int:
        return len(self.transitions)

    def compute_return(self) -> float:
        return sum(t.reward for t in self.transitions)

    def last(self) -> Transition | None:
        return self.transitions[-1] if self.transitions else None
