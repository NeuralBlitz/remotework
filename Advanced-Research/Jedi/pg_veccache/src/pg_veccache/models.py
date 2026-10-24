from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class CacheConfig:
    max_entries: int = 1000
    ttl_seconds: int = 3600
    eviction_policy: str = "lru"
    enable_compression: bool = False

    def validate(self) -> bool:
        return self.max_entries > 0 and self.ttl_seconds > 0


@dataclass
class CacheEntry:
    key: str
    embedding: list[float]
    metadata: dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)

    @property
    def dimension(self) -> int:
        return len(self.embedding)

    def touch(self) -> None:
        self.access_count += 1
        self.last_accessed = datetime.now()
