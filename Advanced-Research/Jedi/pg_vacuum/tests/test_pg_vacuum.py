import pytest

from pg_vacuum.models import TableStats, VacuumConfig, VacuumStrategy
from pg_vacuum.strategies import AggressiveStrategy, BalancedStrategy, StrategyFactory
from pg_vacuum.tuner import VacuumTuner


def _make_stats(
    dead: int = 100,
    live: int = 1000,
    write_rate: float = 50.0,
    size: int = 1_000_000,
) -> TableStats:
    return TableStats(
        schema_name="public",
        table_name="orders",
        dead_tuples=dead,
        live_tuples=live,
        table_size_bytes=size,
        last_autovacuum_age_hours=24.0,
        write_rate_per_second=write_rate,
    )


class TestVacuumConfig:
    def test_default_config(self) -> None:
        cfg = VacuumConfig.default()
        assert cfg.strategy == VacuumStrategy.BALANCED
        assert cfg.vacuum_cost_delay == 2
        assert cfg.vacuum_cost_limit == 200

    def test_frozen(self) -> None:
        cfg = VacuumConfig.default()
        with pytest.raises(AttributeError):
            cfg.vacuum_cost_delay = 99  # type: ignore[misc]


class TestTableStats:
    def test_dead_tuple_ratio(self) -> None:
        stats = _make_stats(dead=100, live=900)
        assert stats.dead_tuple_ratio == pytest.approx(0.1)

    def test_dead_tuple_ratio_empty(self) -> None:
        stats = _make_stats(dead=0, live=0)
        assert stats.dead_tuple_ratio == 0.0

    def test_dead_tuple_ratio_all_dead(self) -> None:
        stats = _make_stats(dead=500, live=0)
        assert stats.dead_tuple_ratio == 1.0


class TestAggressiveStrategy:
    def test_produces_aggressive_config(self) -> None:
        stats = _make_stats(dead=10000, live=50000)
        strategy = AggressiveStrategy()
        cfg = strategy.compute_config(stats)
        assert cfg.strategy == VacuumStrategy.AGGRESSIVE
        assert cfg.vacuum_cost_delay == 0
        assert cfg.vacuum_cost_limit == 2000

    def test_low_scale_factor(self) -> None:
        stats = _make_stats(dead=5000, live=10000)
        cfg = AggressiveStrategy().compute_config(stats)
        assert cfg.autovacuum_vacuum_scale_factor == 0.01


class TestBalancedStrategy:
    def test_produces_balanced_config(self) -> None:
        stats = _make_stats(dead=100, live=1000)
        cfg = BalancedStrategy().compute_config(stats)
        assert cfg.strategy == VacuumStrategy.BALANCED
        assert cfg.vacuum_cost_delay == 2

    def test_default_scale_factor(self) -> None:
        stats = _make_stats()
        cfg = BalancedStrategy().compute_config(stats)
        assert cfg.autovacuum_vacuum_scale_factor == 0.2


class TestStrategyFactory:
    def test_create_aggressive(self) -> None:
        s = StrategyFactory.create(VacuumStrategy.AGGRESSIVE)
        assert isinstance(s, AggressiveStrategy)

    def test_create_balanced(self) -> None:
        s = StrategyFactory.create(VacuumStrategy.BALANCED)
        assert isinstance(s, BalancedStrategy)

    def test_create_returns_correct_type(self) -> None:
        assert isinstance(StrategyFactory.create(VacuumStrategy.AGGRESSIVE), AggressiveStrategy)
        assert isinstance(StrategyFactory.create(VacuumStrategy.BALANCED), BalancedStrategy)


class TestVacuumTuner:
    def test_high_write_selects_aggressive(self) -> None:
        tuner = VacuumTuner()
        stats = _make_stats(write_rate=500.0)
        assert tuner.select_strategy(stats) == VacuumStrategy.AGGRESSIVE

    def test_high_dead_ratio_selects_aggressive(self) -> None:
        tuner = VacuumTuner()
        stats = _make_stats(dead=200, live=100, write_rate=1.0)
        assert tuner.select_strategy(stats) == VacuumStrategy.AGGRESSIVE

    def test_low_traffic_selects_balanced(self) -> None:
        tuner = VacuumTuner()
        stats = _make_stats(dead=5, live=1000, write_rate=10.0)
        assert tuner.select_strategy(stats) == VacuumStrategy.BALANCED

    def test_tune_returns_config(self) -> None:
        tuner = VacuumTuner()
        stats = _make_stats(write_rate=200.0)
        cfg = tuner.tune(stats)
        assert isinstance(cfg, VacuumConfig)
        assert cfg.strategy == VacuumStrategy.AGGRESSIVE

    def test_tune_batch(self) -> None:
        tuner = VacuumTuner()
        stats = [_make_stats(write_rate=10.0), _make_stats(write_rate=500.0)]
        configs = tuner.tune_batch(stats)
        assert len(configs) == 2
        assert configs[0].strategy == VacuumStrategy.BALANCED
        assert configs[1].strategy == VacuumStrategy.AGGRESSIVE
