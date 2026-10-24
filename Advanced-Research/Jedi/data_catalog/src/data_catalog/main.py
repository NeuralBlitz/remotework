"""Data catalog management."""
from __future__ import annotations

from .models import CatalogEntry, DataAsset

__all__ = ["DataAsset", "CatalogEntry", "create_entry", "search_entries"]

def create_entry(
    name: str,
    schema: str,
    location: str,
    metadata: dict[str, str],
) -> CatalogEntry:
    asset = DataAsset(name=name, schema=schema, location=location)
    return CatalogEntry(asset=asset, metadata=metadata)

def search_entries(
    entries: list[CatalogEntry],
    query: str,
) -> list[CatalogEntry]:
    return [
        e for e in entries if query.lower() in e.asset.name.lower()
    ]
