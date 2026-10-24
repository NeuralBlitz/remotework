from __future__ import annotations

from abc import ABC, abstractmethod

from causal_inference.models import CausalGraph, Outcome, Treatment


class Estimator(ABC):
    @abstractmethod
    def estimate(self, graph: CausalGraph, treatment: Treatment, outcome: Outcome) -> float: ...


class PropensityScoreEstimator(Estimator):
    def __init__(self, n_strata: int = 5) -> None:
        self.n_strata = n_strata

    def estimate(self, graph: CausalGraph, treatment: Treatment, outcome: Outcome) -> float:
        if not outcome.values:
            return 0.0
        mid = len(outcome.values) // 2
        if mid == 0:
            return 0.0
        treated_mean = sum(outcome.values[:mid]) / mid
        control_mean = sum(outcome.values[mid:]) / (len(outcome.values) - mid)
        return treated_mean - control_mean


class IVEstimator(Estimator):
    def __init__(self, instrument: str = "") -> None:
        self.instrument = instrument

    def estimate(self, graph: CausalGraph, treatment: Treatment, outcome: Outcome) -> float:
        if len(outcome.values) < 2 or len(treatment.levels) < 2:
            return 0.0
        cov_xy = sum(
            (
                treatment.levels[i % len(treatment.levels)]
                - sum(treatment.levels) / len(treatment.levels)
            )
            * (outcome.values[i] - sum(outcome.values) / len(outcome.values))
            for i in range(min(len(treatment.levels), len(outcome.values)))
        )
        var_x = sum(
            (t - sum(treatment.levels) / len(treatment.levels)) ** 2 for t in treatment.levels
        )
        if var_x == 0:
            return 0.0
        return cov_xy / var_x
