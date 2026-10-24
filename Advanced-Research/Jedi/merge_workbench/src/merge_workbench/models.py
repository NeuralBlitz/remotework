from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class MergeStrategy(Enum):
    SLERP = auto()
    TIES = auto()
    LINEAR = auto()


@dataclass
class MergeConfig:
    strategy: MergeStrategy
    alpha: float = 0.5
    sparsity: float = 0.3
    exclude_patterns: list[str] = field(default_factory=list)

    def validate(self) -> bool:
        return 0.0 <= self.alpha <= 1.0 and 0.0 <= self.sparsity <= 1.0


@dataclass
class MergeResult:
    config: MergeConfig
    merged_params: dict[str, list[float]] = field(default_factory=dict)
    elapsed_ms: float = 0.0
    success: bool = True

    @property
    def param_count(self) -> int:
        return sum(len(v) for v in self.merged_params.values())
