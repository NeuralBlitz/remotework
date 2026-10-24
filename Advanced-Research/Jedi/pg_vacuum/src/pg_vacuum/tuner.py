from __future__ import annotations

from pg_vacuum.models import TableStats, VacuumConfig, VacuumStrategy
from pg_vacuum.strategies import AggressiveStrategy, BalancedStrategy, StrategyFactory

HIGH_WRITE_THRESHOLD = 100.0
HIGH_DEAD_RATIO_THRESHOLD = 0.1


class VacuumTuner:
    def __init__(self) -> None:
        self._aggressive = AggressiveStrategy()
        self._balanced = BalancedStrategy()

    def select_strategy(self, stats: TableStats) -> VacuumStrategy:
        if stats.write_rate_per_second > HIGH_WRITE_THRESHOLD:
            return VacuumStrategy.AGGRESSIVE
        if stats.dead_tuple_ratio > HIGH_DEAD_RATIO_THRESHOLD:
            return VacuumStrategy.AGGRESSIVE
        return VacuumStrategy.BALANCED

    def tune(self, stats: TableStats) -> VacuumConfig:
        strategy = self.select_strategy(stats)
        tuner = StrategyFactory.create(strategy)
        return tuner.compute_config(stats)

    def tune_batch(self, stats_list: list[TableStats]) -> list[VacuumConfig]:
        return [self.tune(s) for s in stats_list]
