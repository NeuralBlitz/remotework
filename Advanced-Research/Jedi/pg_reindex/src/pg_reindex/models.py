from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class IndexInfo:
    schema_name: str
    table_name: str
    index_name: str
    index_size_bytes: int
    table_size_bytes: int
    bloat_ratio: float
    is_unique: bool
    is_primary: bool
    last_reindex_at: datetime | None = None
    index_scan_count: int = 0
    index_tup_read: int = 0
    index_tup_fetch: int = 0

    @property
    def is_bloated(self) -> bool:
        return self.bloat_ratio > 0.3

    @property
    def needs_reindex(self) -> bool:
        return self.is_bloated and self.index_scan_count > 100


@dataclass(frozen=True)
class FragmentationReport:
    schema_name: str
    generated_at: datetime = field(default_factory=datetime.now)
    total_indexes: int = 0
    bloated_indexes: int = 0
    total_bloat_bytes: int = 0
    indexes: list[IndexInfo] = field(default_factory=list)

    @property
    def bloat_percentage(self) -> float:
        if self.total_indexes == 0:
            return 0.0
        return self.bloated_indexes / self.total_indexes

    @property
    def bloated_index_names(self) -> list[str]:
        return [idx.index_name for idx in self.indexes if idx.is_bloated]
