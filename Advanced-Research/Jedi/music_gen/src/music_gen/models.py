from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Note:
    pitch: str = "C4"
    duration: float = 1.0
    velocity: int = 64


@dataclass
class Track:
    track_id: str
    name: str = ""
    instrument: str = "piano"
    notes: list[Note] = field(default_factory=list)


@dataclass
class Composition:
    composition_id: str
    title: str = ""
    bpm: int = 120
    tracks: list[Track] = field(default_factory=list)
    state: str = "draft"

