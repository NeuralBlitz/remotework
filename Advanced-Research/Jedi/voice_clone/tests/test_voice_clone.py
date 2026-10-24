from __future__ import annotations

from voice_clone.builder import SpeakerEmbeddingBuilder, VoiceCloneEngine
from voice_clone.models import SpeakerProfile, VoiceSample


def _make_samples() -> list[VoiceSample]:
    return [
        VoiceSample(sample_id="s1", duration_ms=1000, features=[1.0, 2.0, 3.0]),
        VoiceSample(sample_id="s2", duration_ms=2000, features=[2.0, 3.0, 4.0]),
    ]


def test_builder_creates_profile() -> None:
    builder = SpeakerEmbeddingBuilder()
    for s in _make_samples():
        builder.add_sample(s)
    profile = builder.build(speaker_id="sp1", name="Alice")
    assert profile.sample_count == 2
    assert profile.total_duration_ms == 3000


def test_embedding_averaged() -> None:
    builder = SpeakerEmbeddingBuilder()
    for s in _make_samples():
        builder.add_sample(s)
    profile = builder.build(speaker_id="sp1")
    assert profile.embedding == [1.5, 2.5, 3.5]


def test_empty_builder() -> None:
    builder = SpeakerEmbeddingBuilder()
    profile = builder.build(speaker_id="sp2")
    assert profile.sample_count == 0


def test_voice_clone_engine() -> None:
    engine = VoiceCloneEngine()
    profile = SpeakerProfile(speaker_id="sp1", name="Bob")
    engine.register(profile)
    assert engine.get_profile("sp1") is not None
    assert engine.get_profile("sp2") is None


def test_list_profiles() -> None:
    engine = VoiceCloneEngine()
    engine.register(SpeakerProfile(speaker_id="sp1"))
    engine.register(SpeakerProfile(speaker_id="sp2"))
    assert len(engine.list_profiles()) == 2

