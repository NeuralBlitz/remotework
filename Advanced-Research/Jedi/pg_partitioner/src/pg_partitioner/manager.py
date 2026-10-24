"""Partition manager — orchestrates strategy selection and maintenance."""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

from pg_partitioner.models import MaintenanceResult, PartitionConfig, PartitionType
from pg_partitioner.strategies import (
    HashPartition,
    ListPartition,
    PartitionStrategy,
    RangePartition,
)
from pg_partitioner.worker import MaintenanceWorker

logger = logging.getLogger(__name__)


class PartitionManager:
    """High-level API for managing PostgreSQL table partitions.

    Usage::

        config = PartitionConfig(
            table_name="orders",
            partition_column="created_at",
            partition_type=PartitionType.RANGE,
        )
        manager = PartitionManager(config)

        # Get the CREATE SQL for converting to partitioned table
        print(manager.create_parent_sql())

        # Run monthly maintenance
        result = manager.run_maintenance()
    """

    _strategies: dict[PartitionType, type[PartitionStrategy]] = {
        PartitionType.RANGE: RangePartition,
        PartitionType.LIST: ListPartition,
        PartitionType.HASH: HashPartition,
    }

    def __init__(self, config: PartitionConfig) -> None:
        self.config = config
        self._strategy = self._build_strategy()
        self._worker = MaintenanceWorker(self._strategy)

    @property
    def strategy(self) -> PartitionStrategy:
        return self._strategy

    def create_parent_sql(self) -> str:
        """SQL to convert the table to a partitioned parent."""
        return self._strategy.create_parent_sql()

    def create_partition_sql(self, partition: Any) -> str:
        """SQL to create a specific partition."""
        return self._strategy.create_partition_sql(partition)

    def generate_partitions(self, as_of: date | None = None) -> list[Any]:
        """Generate all partitions that should exist."""
        return self._strategy.generate_partitions(as_of=as_of)

    def run_maintenance(self, as_of: date | None = None) -> MaintenanceResult:
        """Run full maintenance: create upcoming, drop expired."""
        return self._worker.run(as_of=as_of)

    def create_upcoming(
        self, months_ahead: int = 3, as_of: date | None = None
    ) -> MaintenanceResult:
        """Create partitions for the next N months."""
        return self._worker.create_upcoming(months_ahead, as_of=as_of)

    def drop_expired(self, months_behind: int = 12, as_of: date | None = None) -> MaintenanceResult:
        """Drop partitions older than N months."""
        return self._worker.drop_expired(months_behind, as_of=as_of)

    def switch_strategy(self, partition_type: PartitionType) -> None:
        """Dynamically switch the partitioning strategy."""
        logger.info(
            "Switching strategy from %s to %s",
            self.config.partition_type,
            partition_type,
        )
        self.config.partition_type = partition_type
        self._strategy = self._build_strategy()
        self._worker = MaintenanceWorker(self._strategy)

    def _build_strategy(self) -> PartitionStrategy:
        cls = self._strategies.get(self.config.partition_type)
        if cls is None:
            raise ValueError(f"Unknown partition type: {self.config.partition_type}")
        return cls(self.config)
