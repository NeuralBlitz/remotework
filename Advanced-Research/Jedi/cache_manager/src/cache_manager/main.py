"""Cache management utilities."""
from __future__ import annotations

from .models import CacheEntry

__all__ = ["CacheEntry", "create_entry", "is_expired"]

def create_entry(key: str, value: str, ttl: int = 300) -> CacheEntry:
    return CacheEntry(key=key, value=value, ttl=ttl)

def is_expired(entry: CacheEntry) -> bool:
    return entry.is_expired()
