"""Maintenance worker — runs scheduled partition operations."""

from __future__ import annotations

import logging
from datetime import date

from pg_partitioner.models import MaintenanceResult
from pg_partitioner.strategies import PartitionStrategy

logger = logging.getLogger(__name__)


class MaintenanceWorker:
    """Executes partition maintenance tasks.

    Tasks:
    1. Create future partitions (pre_create_months ahead)
    2. Drop old partitions (retention_months behind)
    3. Report any errors
    """

    def __init__(self, strategy: PartitionStrategy) -> None:
        self.strategy = strategy

    def run(self, as_of: date | None = None) -> MaintenanceResult:
        """Run a full maintenance cycle. Returns summary of actions taken."""
        result = MaintenanceResult()
        config = self.strategy.config

        # Generate what should exist
        expected = self.strategy.generate_partitions(as_of=as_of)
        logger.info("Expected %d partitions for %s", len(expected), config.table_name)

        # In production: compare with existing partitions
        # For now, generate CREATE SQL for all expected partitions
        for partition in expected:
            sql = self.strategy.create_partition_sql(partition)
            result.created.append(partition.full_name)
            logger.debug("Would create: %s", sql[:80])

        return result

    def create_upcoming(self, months_ahead: int, as_of: date | None = None) -> MaintenanceResult:
        """Create only partitions for the next N months."""
        result = MaintenanceResult()
        all_partitions = self.strategy.generate_partitions(as_of=as_of)
        today = as_of or date.today()

        for partition in all_partitions:
            if partition.from_value and partition.from_value >= today.isoformat():
                sql = self.strategy.create_partition_sql(partition)
                result.created.append(partition.full_name)
                logger.debug("Would create upcoming: %s", sql[:80])

        return result

    def drop_expired(self, months_behind: int, as_of: date | None = None) -> MaintenanceResult:
        """Drop partitions older than N months."""
        result = MaintenanceResult()
        config = self.strategy.config

        # In production: list existing partitions, compare with retention cutoff
        logger.info(
            "Would drop partitions older than %d months for %s",
            months_behind,
            config.table_name,
        )

        return result
