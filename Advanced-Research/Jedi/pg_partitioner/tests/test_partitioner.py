"""Tests for the Dynamic Table Partitioner."""

from __future__ import annotations

from datetime import date

import pytest

from pg_partitioner.manager import PartitionManager
from pg_partitioner.models import PartitionConfig, PartitionInfo, PartitionType
from pg_partitioner.strategies import HashPartition, ListPartition, RangePartition
from pg_partitioner.worker import MaintenanceWorker


@pytest.fixture
def range_config() -> PartitionConfig:
    return PartitionConfig(
        table_name="orders",
        partition_column="created_at",
        partition_type=PartitionType.RANGE,
        retention_months=12,
        pre_create_months=3,
    )


@pytest.fixture
def list_config() -> PartitionConfig:
    return PartitionConfig(
        table_name="users",
        partition_column="region",
        partition_type=PartitionType.LIST,
        default_list_values=["US", "EU", "ASIA"],
    )


@pytest.fixture
def hash_config() -> PartitionConfig:
    return PartitionConfig(
        table_name="events",
        partition_column="id",
        partition_type=PartitionType.HASH,
        hash_partitions=8,
    )


# ── Range Partition Tests ──────────────────────────────────────────


class TestRangePartition:
    def test_create_parent_sql(self, range_config: PartitionConfig) -> None:
        strategy = RangePartition(range_config)
        sql = strategy.create_parent_sql()
        assert "PARTITION BY RANGE" in sql
        assert "created_at" in sql

    def test_create_partition_sql(self, range_config: PartitionConfig) -> None:
        strategy = RangePartition(range_config)
        partition = PartitionInfo(
            partition_name="2026_01",
            parent_table="orders",
            partition_type=PartitionType.RANGE,
            from_value="2026-01-01",
            to_value="2026-02-01",
        )
        sql = strategy.create_partition_sql(partition)
        assert "orders_2026_01" in sql
        assert "2026-01-01" in sql
        assert "2026-02-01" in sql

    def test_drop_partition_sql(self, range_config: PartitionConfig) -> None:
        strategy = RangePartition(range_config)
        sql = strategy.drop_partition_sql("2025_01")
        assert "DROP TABLE" in sql
        assert "orders_2025_01" in sql

    def test_detach_partition_sql(self, range_config: PartitionConfig) -> None:
        strategy = RangePartition(range_config)
        sql = strategy.detach_partition_sql("2025_01")
        assert "DETACH PARTITION" in sql

    def test_generate_partitions_monthly(self, range_config: PartitionConfig) -> None:
        strategy = RangePartition(range_config)
        today = date(2026, 6, 15)
        partitions = strategy.generate_partitions(as_of=today)

        assert len(partitions) > 0
        # Should include months from June 2025 to September 2026
        names = [p.partition_name for p in partitions]
        assert "2025_06" in names
        assert "2026_06" in names
        # pre_create=3 means partitions go up to (but not including) Sep
        assert "2026_08" in names

    def test_generate_partitions_continuity(self, range_config: PartitionConfig) -> None:
        strategy = RangePartition(range_config)
        partitions = strategy.generate_partitions(as_of=date(2026, 3, 1))

        for i in range(len(partitions) - 1):
            assert partitions[i].to_value == partitions[i + 1].from_value

    def test_generate_correct_count(self, range_config: PartitionConfig) -> None:
        strategy = RangePartition(range_config)
        # retention=12 + pre_create=3 = 15 months
        partitions = strategy.generate_partitions(as_of=date(2026, 1, 1))
        assert len(partitions) == 15


# ── List Partition Tests ───────────────────────────────────────────


class TestListPartition:
    def test_create_parent_sql(self, list_config: PartitionConfig) -> None:
        strategy = ListPartition(list_config)
        sql = strategy.create_parent_sql()
        assert "PARTITION BY LIST" in sql
        assert "region" in sql

    def test_create_partition_sql(self, list_config: PartitionConfig) -> None:
        strategy = ListPartition(list_config)
        partition = PartitionInfo(
            partition_name="us",
            parent_table="users",
            partition_type=PartitionType.LIST,
            list_values=["US"],
        )
        sql = strategy.create_partition_sql(partition)
        assert "users_us" in sql
        assert "'US'" in sql

    def test_generate_partitions_includes_default(self, list_config: PartitionConfig) -> None:
        strategy = ListPartition(list_config)
        partitions = strategy.generate_partitions()

        names = [p.partition_name for p in partitions]
        assert "us" in names
        assert "eu" in names
        assert "asia" in names
        assert "default" in names

    def test_default_partition_sql(self, list_config: PartitionConfig) -> None:
        strategy = ListPartition(list_config)
        partitions = strategy.generate_partitions()
        default = next(p for p in partitions if p.partition_name == "default")
        sql = strategy.create_partition_sql(default)
        assert "DEFAULT" in sql


# ── Hash Partition Tests ───────────────────────────────────────────


class TestHashPartition:
    def test_create_parent_sql(self, hash_config: PartitionConfig) -> None:
        strategy = HashPartition(hash_config)
        sql = strategy.create_parent_sql()
        assert "PARTITION BY HASH" in sql
        assert "id" in sql

    def test_create_partition_sql(self, hash_config: PartitionConfig) -> None:
        strategy = HashPartition(hash_config)
        partition = PartitionInfo(
            partition_name="3",
            parent_table="events",
            partition_type=PartitionType.HASH,
            hash_modulus=8,
            hash_remainder=3,
        )
        sql = strategy.create_partition_sql(partition)
        assert "events_3" in sql
        assert "MODULUS 8" in sql
        assert "REMAINDER 3" in sql

    def test_generate_partitions_correct_count(self, hash_config: PartitionConfig) -> None:
        strategy = HashPartition(hash_config)
        partitions = strategy.generate_partitions()
        assert len(partitions) == 8
        assert all(p.hash_modulus == 8 for p in partitions)

    def test_generate_partitions_covers_all_remainders(self, hash_config: PartitionConfig) -> None:
        strategy = HashPartition(hash_config)
        partitions = strategy.generate_partitions()
        remainders = sorted(p.hash_remainder for p in partitions)
        assert remainders == list(range(8))


# ── Manager Tests ──────────────────────────────────────────────────


class TestPartitionManager:
    def test_range_manager(self, range_config: PartitionConfig) -> None:
        manager = PartitionManager(range_config)
        sql = manager.create_parent_sql()
        assert "RANGE" in sql

    def test_list_manager(self, list_config: PartitionConfig) -> None:
        manager = PartitionManager(list_config)
        sql = manager.create_parent_sql()
        assert "LIST" in sql

    def test_hash_manager(self, hash_config: PartitionConfig) -> None:
        manager = PartitionManager(hash_config)
        sql = manager.create_parent_sql()
        assert "HASH" in sql

    def test_switch_strategy(self, range_config: PartitionConfig) -> None:
        manager = PartitionManager(range_config)
        assert manager.config.partition_type == PartitionType.RANGE

        manager.switch_strategy(PartitionType.HASH)
        assert manager.config.partition_type == PartitionType.HASH
        sql = manager.create_parent_sql()
        assert "HASH" in sql

    def test_run_maintenance(self, range_config: PartitionConfig) -> None:
        manager = PartitionManager(range_config)
        result = manager.run_maintenance(as_of=date(2026, 6, 1))
        assert result.is_clean
        assert len(result.created) > 0

    def test_generate_partitions(self, range_config: PartitionConfig) -> None:
        manager = PartitionManager(range_config)
        partitions = manager.generate_partitions(as_of=date(2026, 1, 1))
        assert len(partitions) == 15

    def test_unknown_type_raises(self) -> None:
        config = PartitionConfig(
            table_name="test",
            partition_column="id",
            partition_type="invalid",  # type: ignore[arg-type]
        )
        with pytest.raises(ValueError, match="Unknown partition type"):
            PartitionManager(config)


# ── MaintenanceWorker Tests ────────────────────────────────────────


class TestMaintenanceWorker:
    def test_run_creates_partitions(self, range_config: PartitionConfig) -> None:
        strategy = RangePartition(range_config)
        worker = MaintenanceWorker(strategy)
        result = worker.run(as_of=date(2026, 6, 1))

        assert result.is_clean
        assert len(result.created) > 0
        assert result.total_actions == len(result.created)

    def test_create_upcoming(self, range_config: PartitionConfig) -> None:
        strategy = RangePartition(range_config)
        worker = MaintenanceWorker(strategy)
        result = worker.create_upcoming(3, as_of=date(2026, 6, 1))

        assert result.is_clean


# ── MonthlyRangeStrategy Tests (the specific example from the prompt) ──


class TestMonthlyRangeStrategy:
    def test_creates_next_month_on_28th(self, range_config: PartitionConfig) -> None:
        """Verify the 28th-of-month auto-creation behavior."""
        strategy = RangePartition(range_config)
        # Simulate running on June 28th
        today = date(2026, 6, 28)
        partitions = strategy.generate_partitions(as_of=today)

        # Should include July (next month)
        names = [p.partition_name for p in partitions]
        assert "2026_07" in names

        # The July partition should exist
        july = next(p for p in partitions if p.partition_name == "2026_07")
        assert july.from_value == "2026-07-01"
        assert july.to_value == "2026-08-01"
