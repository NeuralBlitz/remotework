from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ODEConfig:
    dt: float = 0.01
    t_max: float = 1.0
    tau: float = 1.0
    initial_state: list[float] = field(default_factory=lambda: [0.0])
    method: str = "dopri5"

    def validate(self) -> bool:
        if self.dt <= 0 or self.t_max <= 0:
            return False
        if self.tau <= 0:
            return False
        return len(self.initial_state) > 0


@dataclass
class Trajectory:
    times: list[float] = field(default_factory=list)
    states: list[list[float]] = field(default_factory=list)

    def length(self) -> int:
        return len(self.times)

    def final_state(self) -> list[float]:
        if not self.states:
            return []
        return self.states[-1]

    def state_at(self, t: float) -> list[float]:
        for i, time in enumerate(self.times):
            if time >= t:
                return self.states[i]
        return self.states[-1] if self.states else []
