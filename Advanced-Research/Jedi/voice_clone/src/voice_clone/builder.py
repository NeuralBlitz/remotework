from __future__ import annotations

from .models import SpeakerProfile, VoiceSample


class SpeakerEmbeddingBuilder:
    def __init__(self) -> None:
        self._samples: list[VoiceSample] = []

    def add_sample(self, sample: VoiceSample) -> SpeakerEmbeddingBuilder:
        self._samples.append(sample)
        return self

    def build(self, speaker_id: str, name: str = "") -> SpeakerProfile:
        if not self._samples:
            return SpeakerProfile(speaker_id=speaker_id, name=name)
        total_duration = sum(s.duration_ms for s in self._samples)
        embedding = self._compute_embedding()
        return SpeakerProfile(
            speaker_id=speaker_id,
            name=name,
            sample_count=len(self._samples),
            total_duration_ms=total_duration,
            embedding=embedding,
        )

    def _compute_embedding(self) -> list[float]:
        if not self._samples:
            return []
        dim = len(self._samples[0].features)
        result = [0.0] * dim
        for sample in self._samples:
            for i, val in enumerate(sample.features):
                if i < dim:
                    result[i] += val
        n = len(self._samples)
        return [v / n for v in result]


class VoiceCloneEngine:
    def __init__(self) -> None:
        self._profiles: dict[str, SpeakerProfile] = {}

    def register(self, profile: SpeakerProfile) -> None:
        self._profiles[profile.speaker_id] = profile

    def get_profile(self, speaker_id: str) -> SpeakerProfile | None:
        return self._profiles.get(speaker_id)

    def list_profiles(self) -> list[SpeakerProfile]:
        return list(self._profiles.values())

