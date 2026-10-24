"""Tests for config_manager."""
from __future__ import annotations

from src.config_manager import create_config, create_section, get_value


def test_create_config():
    cfg = create_config("setting1", "value1")
    assert cfg.key == "setting1"
    assert cfg.value == "value1"
    assert cfg.source == "default"

def test_create_config_custom_source():
    cfg = create_config("setting1", "value1", source="env")
    assert cfg.source == "env"

def test_create_section():
    section = create_section("database", [])
    assert section.name == "database"
    assert len(section.configs) == 0

def test_create_section_with_configs():
    configs = [
        create_config("host", "localhost"),
        create_config("port", "5432"),
    ]
    section = create_section("db", configs)
    assert len(section.configs) == 2

def test_get_value_found():
    configs = [create_config("key", "found_value")]
    section = create_section("test", configs)
    assert get_value(section, "key") == "found_value"

def test_get_value_not_found():
    section = create_section("test", [])
    assert get_value(section, "nonexistent") is None

def test_multiple_configs():
    configs = [
        create_config("a", "1"),
        create_config("b", "2"),
        create_config("c", "3"),
    ]
    section = create_section("multi", configs)
    assert get_value(section, "a") == "1"
    assert get_value(section, "b") == "2"
    assert get_value(section, "c") == "3"
