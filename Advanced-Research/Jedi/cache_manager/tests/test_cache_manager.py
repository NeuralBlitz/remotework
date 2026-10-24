"""Tests for cache_manager."""
from __future__ import annotations

from src.cache_manager import create_entry, is_expired


def test_create_entry():
    entry = create_entry("key1", "value1")
    assert entry.key == "key1"
    assert entry.value == "value1"

def test_create_entry_with_ttl():
    entry = create_entry("key1", "value1", ttl=60)
    assert entry.ttl == 60

def test_is_expired():
    entry = create_entry("key1", "value1", ttl=0)
    assert is_expired(entry) is False

def test_entry_default_ttl():
    entry = create_entry("key1", "value1")
    assert entry.ttl == 300

def test_multiple_entries():
    e1 = create_entry("a", "1")
    e2 = create_entry("b", "2")
    assert e1.key != e2.key

def test_entry_is_expired_method():
    entry = create_entry("key1", "value1")
    assert entry.is_expired() is False
