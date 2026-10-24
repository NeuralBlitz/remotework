from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Config:
    key: str
    value: str
    source: str

@dataclass
class ConfigSection:
    name: str
    configs: list[Config] = field(default_factory=list)
