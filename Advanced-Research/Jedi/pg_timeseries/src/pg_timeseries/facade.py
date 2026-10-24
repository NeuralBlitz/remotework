from __future__ import annotations

from pg_timeseries.models import (
    AggregateQuery,
    ChunkInfo,
    CompressionPolicy,
    HypertableConfig,
)


class HypertableFacade:
    def __init__(self) -> None:
        self._hypertables: dict[str, HypertableConfig] = {}
        self._chunks: dict[str, list[ChunkInfo]] = {}
        self._aggregates: dict[str, AggregateQuery] = {}
        self._compressed: set[str] = set()

    def create_hypertable(self, config: HypertableConfig) -> bool:
        if not config.validate():
            raise ValueError(f"Invalid hypertable config: {config.table_name}")
        if config.table_name in self._hypertables:
            raise ValueError(f"Hypertable already exists: {config.table_name}")
        self._hypertables[config.table_name] = config
        self._chunks[config.table_name] = []
        return True

    def drop_hypertable(self, table_name: str, cascade: bool = False) -> bool:
        if table_name not in self._hypertables:
            raise KeyError(f"Hypertable not found: {table_name}")
        del self._hypertables[table_name]
        del self._chunks[table_name]
        self._compressed.discard(table_name)
        to_remove = [k for k, v in self._aggregates.items() if v.source_table == table_name]
        for k in to_remove:
            del self._aggregates[k]
        return True

    def compress_chunks(self, table_name: str) -> int:
        if table_name not in self._hypertables:
            raise KeyError(f"Hypertable not found: {table_name}")
        count = 0
        for chunk in self._chunks[table_name]:
            if not chunk.is_compressed:
                self._chunks[table_name][self._chunks[table_name].index(chunk)] = ChunkInfo(
                    chunk_name=chunk.chunk_name,
                    hypertable_name=chunk.hypertable_name,
                    range_start=chunk.range_start,
                    range_end=chunk.range_end,
                    is_compressed=True,
                    size_bytes=int(chunk.size_bytes * 0.4),
                )
                count += 1
        self._compressed.add(table_name)
        return count

    def create_continuous_aggregate(self, query: AggregateQuery) -> bool:
        if query.source_table not in self._hypertables:
            raise KeyError(f"Source hypertable not found: {query.source_table}")
        if query.name in self._aggregates:
            raise ValueError(f"Aggregate already exists: {query.name}")
        self._aggregates[query.name] = query
        return True

    def add_chunk(self, chunk: ChunkInfo) -> None:
        if chunk.hypertable_name not in self._chunks:
            raise KeyError(f"Hypertable not found: {chunk.hypertable_name}")
        self._chunks[chunk.hypertable_name].append(chunk)

    def get_chunks(self, table_name: str) -> list[ChunkInfo]:
        return list(self._chunks.get(table_name, []))

    def get_hypertable(self, table_name: str) -> HypertableConfig | None:
        return self._hypertables.get(table_name)

    def list_hypertables(self) -> list[str]:
        return list(self._hypertables.keys())

    def list_aggregates(self) -> list[str]:
        return list(self._aggregates.keys())

    def is_compressed(self, table_name: str) -> bool:
        return table_name in self._compressed

    def get_compression_policy(self, table_name: str) -> CompressionPolicy | None:
        config = self._hypertables.get(table_name)
        return config.compression_policy if config else None
