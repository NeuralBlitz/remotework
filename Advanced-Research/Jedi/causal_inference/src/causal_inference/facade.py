from __future__ import annotations

from dataclasses import dataclass, field

from causal_inference.estimators import Estimator, PropensityScoreEstimator
from causal_inference.models import CausalGraph, Outcome, Treatment


@dataclass
class CausalResult:
    ate: float
    estimator_used: str
    refuted: bool = False
    refute_ate: float = 0.0

    @property
    def robust(self) -> bool:
        if not self.refuted:
            return True
        if self.ate == 0:
            return self.refute_ate == 0
        return abs(self.ate - self.refute_ate) / abs(self.ate) < 0.5


class CausalFacade:
    def __init__(self, graph: CausalGraph) -> None:
        self.graph = graph

    def identify(self, treatment: Treatment, outcome: Outcome) -> bool:
        return treatment.name in self.graph.nodes and outcome.name in self.graph.nodes

    def estimate(
        self,
        treatment: Treatment,
        outcome: Outcome,
        estimator: Estimator | None = None,
    ) -> float:
        if estimator is None:
            estimator = PropensityScoreEstimator()
        return estimator.estimate(self.graph, treatment, outcome)

    def refute(self, treatment: Treatment, outcome: Outcome) -> float:
        noisy_outcome = Outcome(
            name=outcome.name,
            values=[v + 0.1 * (i % 2) for i, v in enumerate(outcome.values)],
        )
        return PropensityScoreEstimator().estimate(self.graph, treatment, noisy_outcome)

    def run(
        self,
        treatment: Treatment,
        outcome: Outcome,
        estimator: Estimator | None = None,
    ) -> CausalResult:
        identified = self.identify(treatment, outcome)
        if not identified:
            return CausalResult(ate=0.0, estimator_used="none")
        ate = self.estimate(treatment, outcome, estimator)
        refute_ate = self.refute(treatment, outcome)
        est_name = type(estimator).__name__ if estimator else "PropensityScoreEstimator"
        return CausalResult(
            ate=ate,
            estimator_used=est_name,
            refuted=True,
            refute_ate=refute_ate,
        )
