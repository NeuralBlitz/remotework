from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class LSNPosition:
    segment: int
    offset: int

    def __str__(self) -> str:
        return f"{self.segment}/{self.offset}"


@dataclass
class Memento:
    lsn: LSNPosition
    state: dict[str, object] = field(default_factory=dict)
    label: str = ""
