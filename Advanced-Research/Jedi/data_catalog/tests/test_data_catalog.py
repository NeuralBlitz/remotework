"""Tests for data_catalog."""
from __future__ import annotations

from src.data_catalog import create_entry, search_entries
from src.data_catalog.models import CatalogEntry, DataAsset


def test_create_entry():
    entry = create_entry("test", "public", "s3://bucket/path", {"owner": "team"})
    assert entry.asset.name == "test"
    assert entry.asset.schema == "public"

def test_create_entry_to_dict():
    entry = create_entry("test", "public", "s3://bucket/path", {})
    d = entry.to_dict()
    assert "asset" in d
    assert "metadata" in d

def test_search_entries_empty():
    result = search_entries([], "test")
    assert len(result) == 0

def test_search_entries_found():
    entries = [
        CatalogEntry(
            asset=DataAsset(name="table1", schema="public", location=""),
            metadata={},
        ),
        CatalogEntry(
            asset=DataAsset(name="table2", schema="public", location=""),
            metadata={},
        ),
    ]
    result = search_entries(entries, "table1")
    assert len(result) == 1

def test_search_entries_case_insensitive():
    entries = [
        CatalogEntry(
            asset=DataAsset(name="TableA", schema="public", location=""),
            metadata={},
        )
    ]
    result = search_entries(entries, "tablea")
    assert len(result) == 1

def test_search_entries_no_match():
    entries = [
        CatalogEntry(
            asset=DataAsset(name="table1", schema="public", location=""),
            metadata={},
        )
    ]
    result = search_entries(entries, "xyz")
    assert len(result) == 0
