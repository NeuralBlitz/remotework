from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TextRequest:
    text: str
    voice: str = "default"
    speed: float = 1.0


@dataclass
class AudioOutput:
    duration_ms: int = 0
    sample_rate: int = 22050
    phoneme_count: int = 0
    raw_data: bytes = b""

