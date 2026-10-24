from __future__ import annotations

from abc import ABC, abstractmethod
import time

from merge_workbench.models import MergeConfig, MergeResult


class MergeTemplate(ABC):
    def __init__(self, config: MergeConfig) -> None:
        self.config = config

    def load(self, model_a: dict[str, list[float]], model_b: dict[str, list[float]]) -> None:
        self.model_a = model_a
        self.model_b = model_b

    @abstractmethod
    def align(self) -> None: ...

    @abstractmethod
    def merge(self) -> dict[str, list[float]]: ...

    def save(self, merged: dict[str, list[float]]) -> MergeResult:
        return MergeResult(config=self.config, merged_params=merged)

    def run(
        self,
        model_a: dict[str, list[float]],
        model_b: dict[str, list[float]],
    ) -> MergeResult:
        start = time.time()
        self.load(model_a, model_b)
        self.align()
        merged = self.merge()
        elapsed = (time.time() - start) * 1000
        result = self.save(merged)
        result.elapsed_ms = elapsed
        return result


class SlerpMerger(MergeTemplate):
    def align(self) -> None:
        pass

    def merge(self) -> dict[str, list[float]]:
        alpha = self.config.alpha
        merged: dict[str, list[float]] = {}
        for key in self.model_a:
            if key in self.model_b:
                a, b = self.model_a[key], self.model_b[key]
                merged[key] = [
                    a[i] * (1 - alpha) + b[i] * alpha for i in range(min(len(a), len(b)))
                ]
            else:
                merged[key] = list(self.model_a[key])
        return merged


class TiesMerger(MergeTemplate):
    def align(self) -> None:
        pass

    def merge(self) -> dict[str, list[float]]:
        alpha = self.config.alpha
        sparsity = self.config.sparsity
        merged: dict[str, list[float]] = {}
        for key in self.model_a:
            if key in self.model_b:
                a, b = self.model_a[key], self.model_b[key]
                n = min(len(a), len(b))
                raw = [a[i] * (1 - alpha) + b[i] * alpha for i in range(n)]
                threshold = sorted(abs(x) for x in raw)[int(n * sparsity)] if n > 0 else 0
                merged[key] = [v if abs(v) >= threshold else 0.0 for v in raw]
            else:
                merged[key] = list(self.model_a[key])
        return merged
