"""Configuration management."""
from __future__ import annotations

from .models import Config, ConfigSection

__all__ = ["Config", "ConfigSection", "create_config", "create_section", "get_value"]

def create_config(key: str, value: str, source: str = "default") -> Config:
    return Config(key=key, value=value, source=source)

def create_section(name: str, configs: list[Config]) -> ConfigSection:
    return ConfigSection(name=name, configs=configs)

def get_value(section: ConfigSection, key: str) -> str | None:
    for cfg in section.configs:
        if cfg.key == key:
            return cfg.value
    return None
