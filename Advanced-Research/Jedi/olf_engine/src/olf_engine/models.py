from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class ScentProfile:
    molecule_id: str
    intensity: float = 0.0
    pleasantness: float = 0.0
    descriptors: list[str] = field(default_factory=list)
