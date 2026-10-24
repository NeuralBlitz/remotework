from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class VoiceSample:
    sample_id: str
    duration_ms: int = 0
    features: list[float] = field(default_factory=list)
    sample_rate: int = 22050


@dataclass
class SpeakerProfile:
    speaker_id: str
    name: str = ""
    sample_count: int = 0
    total_duration_ms: int = 0
    embedding: list[float] = field(default_factory=list)

