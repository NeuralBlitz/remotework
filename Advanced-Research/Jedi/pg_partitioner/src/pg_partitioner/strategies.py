"""Partition strategies — Strategy Pattern for different partitioning methods."""

from __future__ import annotations

import abc
import logging
from datetime import date

from pg_partitioner.models import PartitionConfig, PartitionInfo, PartitionType

logger = logging.getLogger(__name__)


class PartitionStrategy(abc.ABC):
    """Abstract base for partition strategies."""

    def __init__(self, config: PartitionConfig) -> None:
        self.config = config

    @abc.abstractmethod
    def create_parent_sql(self) -> str:
        """SQL to convert a table to a partitioned parent."""
        ...

    @abc.abstractmethod
    def create_partition_sql(self, partition: PartitionInfo) -> str:
        """SQL to create a single partition."""
        ...

    @abc.abstractmethod
    def detach_partition_sql(self, partition_name: str) -> str:
        """SQL to detach a partition."""
        ...

    @abc.abstractmethod
    def drop_partition_sql(self, partition_name: str) -> str:
        """SQL to drop a partition."""
        ...

    @abc.abstractmethod
    def generate_partitions(self, as_of: date | None = None) -> list[PartitionInfo]:
        """Generate partition definitions that should exist."""
        ...

    @abc.abstractmethod
    def list_partitions_sql(self) -> str:
        """SQL to list existing partitions."""
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(table={self.config.table_name})"


class RangePartition(PartitionStrategy):
    """Range-based partitioning — typically by date (monthly).

    Best for: Time-series data, event logs, append-heavy workloads.
    Example: `orders_2026_01`, `orders_2026_02`, etc.
    """

    def create_parent_sql(self) -> str:
        return (
            f"ALTER TABLE {self.config.schema_name}.{self.config.table_name} "
            f"PARTITION BY RANGE ({self.config.partition_column})"
        )

    def create_partition_sql(self, partition: PartitionInfo) -> str:
        return (
            f"CREATE TABLE IF NOT EXISTS {self.config.schema_name}.{partition.full_name} "
            f"PARTITION OF {self.config.schema_name}.{self.config.table_name} "
            f"FOR VALUES FROM ('{partition.from_value}') TO ('{partition.to_value}')"
        )

    def detach_partition_sql(self, partition_name: str) -> str:
        full = f"{self.config.table_name}_{partition_name}"
        table = f"{self.config.schema_name}.{self.config.table_name}"
        return f"ALTER TABLE {table} DETACH PARTITION {full}"

    def drop_partition_sql(self, partition_name: str) -> str:
        full = f"{self.config.table_name}_{partition_name}"
        return f"DROP TABLE IF EXISTS {self.config.schema_name}.{full}"

    def generate_partitions(self, as_of: date | None = None) -> list[PartitionInfo]:
        """Generate monthly partitions from (now - retention) to (now + pre_create)."""
        today = as_of or date.today()
        start = self._month_start(today.year, today.month)
        start = self._add_months(start, -self.config.retention_months)
        end = self._add_months(today, self.config.pre_create_months)

        partitions: list[PartitionInfo] = []
        current = start
        while current < end:
            next_month = self._add_months(current, 1)
            name = current.strftime("%Y_%m")
            partitions.append(
                PartitionInfo(
                    partition_name=name,
                    parent_table=self.config.table_name,
                    partition_type=PartitionType.RANGE,
                    from_value=current.isoformat(),
                    to_value=next_month.isoformat(),
                )
            )
            current = next_month

        return partitions

    def list_partitions_sql(self) -> str:
        return (
            f"SELECT inhrelid::regclass::text AS partition_name "
            f"FROM pg_inherits "
            f"WHERE inhparent = '{self.config.schema_name}.{self.config.table_name}'::regclass"
        )

    @staticmethod
    def _month_start(year: int, month: int) -> date:
        return date(year, month, 1)

    @staticmethod
    def _add_months(d: date, months: int) -> date:
        month = d.month + months
        year = d.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        return date(year, month, 1)


class ListPartition(PartitionStrategy):
    """List-based partitioning — by categorical values.

    Best for: Region-based data, status enums, tenant isolation.
    Example: `orders_US`, `orders_EU`, `orders_ASIA`.
    """

    def create_parent_sql(self) -> str:
        return (
            f"ALTER TABLE {self.config.schema_name}.{self.config.table_name} "
            f"PARTITION BY LIST ({self.config.partition_column})"
        )

    def create_partition_sql(self, partition: PartitionInfo) -> str:
        values = ", ".join(f"'{v}'" for v in (partition.list_values or []))
        return (
            f"CREATE TABLE IF NOT EXISTS {self.config.schema_name}.{partition.full_name} "
            f"PARTITION OF {self.config.schema_name}.{self.config.table_name} "
            f"FOR VALUES IN ({values})"
        )

    def detach_partition_sql(self, partition_name: str) -> str:
        full = f"{self.config.table_name}_{partition_name}"
        tbl = f"{self.config.schema_name}.{self.config.table_name}"
        return f"ALTER TABLE {tbl} DETACH PARTITION {full}"

    def drop_partition_sql(self, partition_name: str) -> str:
        full = f"{self.config.table_name}_{partition_name}"
        return f"DROP TABLE IF EXISTS {self.config.schema_name}.{full}"

    def generate_partitions(self, as_of: date | None = None) -> list[PartitionInfo]:
        """Generate one partition per list value + a default partition."""
        partitions: list[PartitionInfo] = []
        for value in self.config.default_list_values:
            partitions.append(
                PartitionInfo(
                    partition_name=value.lower(),
                    parent_table=self.config.table_name,
                    partition_type=PartitionType.LIST,
                    list_values=[value],
                )
            )
        # Always add a default partition for unknown values
        partitions.append(
            PartitionInfo(
                partition_name="default",
                parent_table=self.config.table_name,
                partition_type=PartitionType.LIST,
                list_values=["DEFAULT"],
            )
        )
        return partitions

    def list_partitions_sql(self) -> str:
        return (
            f"SELECT inhrelid::regclass::text AS partition_name "
            f"FROM pg_inherits "
            f"WHERE inhparent = '{self.config.schema_name}.{self.config.table_name}'::regclass"
        )


class HashPartition(PartitionStrategy):
    """Hash-based partitioning — uniform distribution.

    Best for: Even distribution of writes, no natural partition key.
    Example: `events_0`, `events_1`, ..., `events_15`.
    """

    def create_parent_sql(self) -> str:
        return (
            f"ALTER TABLE {self.config.schema_name}.{self.config.table_name} "
            f"PARTITION BY HASH ({self.config.partition_column})"
        )

    def create_partition_sql(self, partition: PartitionInfo) -> str:
        schema = self.config.schema_name
        return (
            f"CREATE TABLE IF NOT EXISTS {schema}.{partition.full_name} "
            f"PARTITION OF {schema}.{self.config.table_name} "
            f"FOR VALUES WITH "
            f"(MODULUS {partition.hash_modulus}, REMAINDER {partition.hash_remainder})"
        )

    def detach_partition_sql(self, partition_name: str) -> str:
        full = f"{self.config.table_name}_{partition_name}"
        tbl = f"{self.config.schema_name}.{self.config.table_name}"
        return f"ALTER TABLE {tbl} DETACH PARTITION {full}"

    def drop_partition_sql(self, partition_name: str) -> str:
        full = f"{self.config.table_name}_{partition_name}"
        return f"DROP TABLE IF EXISTS {self.config.schema_name}.{full}"

    def generate_partitions(self, as_of: date | None = None) -> list[PartitionInfo]:
        """Generate N hash partitions (0 through modulus-1)."""
        partitions: list[PartitionInfo] = []
        for i in range(self.config.hash_partitions):
            partitions.append(
                PartitionInfo(
                    partition_name=str(i),
                    parent_table=self.config.table_name,
                    partition_type=PartitionType.HASH,
                    hash_modulus=self.config.hash_partitions,
                    hash_remainder=i,
                )
            )
        return partitions

    def list_partitions_sql(self) -> str:
        return (
            f"SELECT inhrelid::regclass::text AS partition_name "
            f"FROM pg_inherits "
            f"WHERE inhparent = '{self.config.schema_name}.{self.config.table_name}'::regclass"
        )
