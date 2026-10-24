from __future__ import annotations

from datetime import timedelta

from pg_purge.models import ArchiveConfig, PurgeJob, PurgeStrategy


class PurgeJobBuilder:
    def __init__(self) -> None:
        self._name: str = ""
        self._from_table: str = ""
        self._from_schema: str = "public"
        self._where_older_than: timedelta = timedelta(days=90)
        self._timestamp_column: str = "created_at"
        self._archive_config: ArchiveConfig | None = None
        self._strategy: PurgeStrategy = PurgeStrategy.DELETE
        self._batch_size: int = 10000
        self._dry_run: bool = False
        self._extra_conditions: str = ""

    def with_name(self, name: str) -> PurgeJobBuilder:
        self._name = name
        return self

    def from_table(self, table: str, schema: str = "public") -> PurgeJobBuilder:
        self._from_table = table
        self._from_schema = schema
        return self

    def where_older_than(
        self,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
    ) -> PurgeJobBuilder:
        self._where_older_than = timedelta(days=days, hours=hours, minutes=minutes)
        return self

    def with_timestamp_column(self, column: str) -> PurgeJobBuilder:
        self._timestamp_column = column
        return self

    def archive_to(self, archive_table: str, schema: str = "archive") -> PurgeJobBuilder:
        self._archive_config = ArchiveConfig(
            archive_table=archive_table,
            archive_schema=schema,
        )
        self._strategy = PurgeStrategy.ARCHIVE_THEN_DELETE
        return self

    def archive_only(self, archive_table: str, schema: str = "archive") -> PurgeJobBuilder:
        self._archive_config = ArchiveConfig(
            archive_table=archive_table,
            archive_schema=schema,
        )
        self._strategy = PurgeStrategy.ARCHIVE_ONLY
        return self

    def with_strategy(self, strategy: PurgeStrategy) -> PurgeJobBuilder:
        self._strategy = strategy
        return self

    def with_batch_size(self, size: int) -> PurgeJobBuilder:
        self._batch_size = size
        return self

    def with_extra_conditions(self, conditions: str) -> PurgeJobBuilder:
        self._extra_conditions = conditions
        return self

    def dry_run(self, enabled: bool = True) -> PurgeJobBuilder:
        self._dry_run = enabled
        return self

    def build(self) -> PurgeJob:
        if not self._name:
            raise ValueError("Job name is required")
        if not self._from_table:
            raise ValueError("Source table is required")

        return PurgeJob(
            name=self._name,
            from_table=self._from_table,
            from_schema=self._from_schema,
            where_older_than=self._where_older_than,
            timestamp_column=self._timestamp_column,
            archive_config=self._archive_config,
            strategy=self._strategy,
            batch_size=self._batch_size,
            dry_run=self._dry_run,
            extra_conditions=self._extra_conditions,
        )
