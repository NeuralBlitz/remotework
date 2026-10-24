from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class VADState(Enum):
    SILENCE = "silence"
    SPEECH = "speech"
    UNCERTAIN = "uncertain"


@dataclass
class AudioChunk:
    samples: list[float] = field(default_factory=list)
    sample_rate: int = 16000
    timestamp_ms: int = 0
    vad_state: VADState = VADState.UNCERTAIN

    def duration_ms(self) -> float:
        if self.sample_rate == 0:
            return 0.0
        return len(self.samples) / self.sample_rate * 1000

    def is_speech(self) -> bool:
        return self.vad_state == VADState.SPEECH


@dataclass
class SpeakerSegment:
    speaker_id: str = ""
    start_ms: int = 0
    end_ms: int = 0
    embedding: list[float] = field(default_factory=list)
    confidence: float = 0.0

    def duration_ms(self) -> int:
        return self.end_ms - self.start_ms

    def is_valid(self) -> bool:
        return self.end_ms > self.start_ms and self.confidence >= 0.0
