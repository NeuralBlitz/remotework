from __future__ import annotations

from abc import ABC, abstractmethod

from speech_diar.models import AudioChunk, SpeakerSegment, VADState


class AudioHandler(ABC):
    def __init__(self) -> None:
        self._next: AudioHandler | None = None

    def set_next(self, handler: AudioHandler) -> AudioHandler:
        self._next = handler
        return handler

    def handle(self, chunk: AudioChunk, segments: list[SpeakerSegment]) -> list[SpeakerSegment]:
        result = self.process(chunk, segments)
        if self._next is not None:
            return self._next.handle(chunk, result)
        return result

    @abstractmethod
    def process(
        self, chunk: AudioChunk, segments: list[SpeakerSegment]
    ) -> list[SpeakerSegment]: ...


class VADEmbeddingHandler(AudioHandler):
    def __init__(self, energy_threshold: float = 0.01) -> None:
        super().__init__()
        self._threshold = energy_threshold

    def process(self, chunk: AudioChunk, segments: list[SpeakerSegment]) -> list[SpeakerSegment]:
        if not chunk.samples:
            chunk.vad_state = VADState.SILENCE
            return segments
        energy = sum(s * s for s in chunk.samples) / len(chunk.samples)
        chunk.vad_state = VADState.SPEECH if energy > self._threshold else VADState.SILENCE
        if chunk.is_speech():
            embedding = [sum(chunk.samples) / len(chunk.samples)] * 8
            seg = SpeakerSegment(
                speaker_id="unknown",
                start_ms=chunk.timestamp_ms,
                end_ms=chunk.timestamp_ms + int(chunk.duration_ms()),
                embedding=embedding,
                confidence=min(1.0, energy / self._threshold),
            )
            segments.append(seg)
        return segments


class ClusteringHandler(AudioHandler):
    def __init__(self, num_speakers: int = 2) -> None:
        super().__init__()
        self._num_speakers = num_speakers
        self._speaker_centers: dict[str, list[float]] = {}

    def process(self, chunk: AudioChunk, segments: list[SpeakerSegment]) -> list[SpeakerSegment]:
        for seg in segments:
            if seg.speaker_id == "unknown":
                seg.speaker_id = self._assign_speaker(seg.embedding)
        return segments

    def _assign_speaker(self, embedding: list[float]) -> str:
        if not embedding:
            return "spk_0"
        center_val = sum(embedding) / len(embedding)
        for spk_id, center in self._speaker_centers.items():
            if center and abs(center_val - sum(center) / len(center)) < 0.5:
                return spk_id
        idx = len(self._speaker_centers)
        if idx >= self._num_speakers:
            return f"spk_{idx % self._num_speakers}"
        spk_id = f"spk_{idx}"
        self._speaker_centers[spk_id] = list(embedding)
        return spk_id


class AudioChain:
    def __init__(self) -> None:
        self._head: AudioHandler | None = None
        self._tail: AudioHandler | None = None

    def add_handler(self, handler: AudioHandler) -> AudioChain:
        if self._head is None:
            self._head = handler
            self._tail = handler
        else:
            assert self._tail is not None
            self._tail.set_next(handler)
            self._tail = handler
        return self

    def process(self, chunk: AudioChunk) -> list[SpeakerSegment]:
        if self._head is None:
            return []
        return self._head.handle(chunk, [])
