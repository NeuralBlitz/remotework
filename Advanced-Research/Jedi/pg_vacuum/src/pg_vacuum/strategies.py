from __future__ import annotations

from abc import ABC, abstractmethod

from pg_vacuum.models import TableStats, VacuumConfig, VacuumStrategy


class VacuumTuningStrategy(ABC):
    @abstractmethod
    def compute_config(self, stats: TableStats) -> VacuumConfig:
        pass


class AggressiveStrategy(VacuumTuningStrategy):
    def compute_config(self, stats: TableStats) -> VacuumConfig:
        threshold = min(25, max(10, stats.dead_tuples // 1000))
        return VacuumConfig(
            vacuum_cost_delay=0,
            vacuum_cost_limit=2000,
            autovacuum_vacuum_threshold=threshold,
            autovacuum_vacuum_scale_factor=0.01,
            autovacuum_analyze_threshold=threshold,
            autovacuum_analyze_scale_factor=0.005,
            strategy=VacuumStrategy.AGGRESSIVE,
        )


class BalancedStrategy(VacuumTuningStrategy):
    def compute_config(self, stats: TableStats) -> VacuumConfig:
        threshold = min(100, max(50, stats.dead_tuples // 5000))
        return VacuumConfig(
            vacuum_cost_delay=2,
            vacuum_cost_limit=200,
            autovacuum_vacuum_threshold=threshold,
            autovacuum_vacuum_scale_factor=0.2,
            autovacuum_analyze_threshold=threshold,
            autovacuum_analyze_scale_factor=0.1,
            strategy=VacuumStrategy.BALANCED,
        )


_STRATEGY_MAP: dict[VacuumStrategy, type[VacuumTuningStrategy]] = {
    VacuumStrategy.AGGRESSIVE: AggressiveStrategy,
    VacuumStrategy.BALANCED: BalancedStrategy,
}


class StrategyFactory:
    @staticmethod
    def create(strategy: VacuumStrategy) -> VacuumTuningStrategy:
        cls = _STRATEGY_MAP.get(strategy)
        if cls is None:
            raise ValueError(f"Unknown strategy: {strategy}")
        return cls()
