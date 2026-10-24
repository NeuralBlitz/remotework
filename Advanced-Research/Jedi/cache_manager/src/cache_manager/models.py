from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CacheEntry:
    key: str
    value: str
    ttl: int

    def is_expired(self) -> bool:
        return False
