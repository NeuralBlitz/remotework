from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SyntheticConfig:
    num_rows: int = 1000
    num_columns: int = 10
    noise_level: float = 0.1
    seed: int = 42
    privacy_epsilon: float = 1.0
    privacy_delta: float = 1e-5

    def validate(self) -> bool:
        if self.num_rows <= 0 or self.num_columns <= 0:
            return False
        if not 0 <= self.noise_level <= 1:
            return False
        return self.privacy_epsilon > 0


@dataclass
class PrivacyMetrics:
    epsilon_used: float = 0.0
    delta_used: float = 0.0
    k_anonymity: int = 0
    l_diversity: int = 0
    uniqueness_ratio: float = 0.0

    def is_private(self, threshold: float = 0.1) -> bool:
        return self.uniqueness_ratio < threshold

    def budget_remaining(self, total_epsilon: float) -> float:
        return max(0.0, total_epsilon - self.epsilon_used)
