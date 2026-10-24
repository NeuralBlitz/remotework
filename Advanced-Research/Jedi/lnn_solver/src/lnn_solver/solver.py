from __future__ import annotations

from lnn_solver.models import ODEConfig, Trajectory
from lnn_solver.strategies import SolverStrategy, Dopri5Strategy


class LNNSolver:
    def __init__(self, strategy: SolverStrategy | None = None) -> None:
        self._strategy = strategy or Dopri5Strategy()

    def set_strategy(self, strategy: SolverStrategy) -> None:
        self._strategy = strategy

    def solve(self, config: ODEConfig) -> Trajectory:
        return self._strategy.solve(config)

    def current_method(self) -> str:
        return self._strategy.name()

    def compare(self, config: ODEConfig, strategies: list[SolverStrategy]) -> dict[str, Trajectory]:
        results: dict[str, Trajectory] = {}
        for strat in strategies:
            results[strat.name()] = strat.solve(config)
        return results
