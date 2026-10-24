import pytest

from speech_diar.chain import AudioChain, ClusteringHandler, VADEmbeddingHandler
from speech_diar.models import AudioChunk, SpeakerSegment, VADState


def test_vad_detects_speech():
    handler = VADEmbeddingHandler(energy_threshold=0.001)
    chunk = AudioChunk(samples=[0.5, -0.5, 0.5, -0.5], timestamp_ms=0)
    segments = handler.handle(chunk, [])
    assert chunk.vad_state == VADState.SPEECH
    assert len(segments) == 1


def test_vad_detects_silence():
    handler = VADEmbeddingHandler(energy_threshold=1.0)
    chunk = AudioChunk(samples=[0.001, 0.001], timestamp_ms=0)
    segments = handler.handle(chunk, [])
    assert chunk.vad_state == VADState.SILENCE
    assert len(segments) == 0


def test_clustering_assigns_speakers():
    chain = AudioChain()
    chain.add_handler(VADEmbeddingHandler(0.001))
    chain.add_handler(ClusteringHandler(num_speakers=2))
    segs1 = chain.process(AudioChunk(samples=[1.0, -1.0], timestamp_ms=0))
    segs2 = chain.process(AudioChunk(samples=[1.0, -1.0], timestamp_ms=100))
    assert len(segs1) == 1
    assert segs1[0].speaker_id == "spk_0"


def test_empty_chain():
    chain = AudioChain()
    assert chain.process(AudioChunk(samples=[1.0])) == []


def test_segment_validity():
    seg = SpeakerSegment(speaker_id="spk_0", start_ms=0, end_ms=100, confidence=0.9)
    assert seg.is_valid()
    assert seg.duration_ms() == 100


def test_invalid_segment():
    seg = SpeakerSegment(start_ms=100, end_ms=0)
    assert not seg.is_valid()


def test_chunk_duration():
    chunk = AudioChunk(samples=[0.0] * 1600, sample_rate=16000)
    assert chunk.duration_ms() == 100.0


def test_full_chain():
    chain = AudioChain()
    chain.add_handler(VADEmbeddingHandler(0.001))
    chain.add_handler(ClusteringHandler(num_speakers=3))
    segments = chain.process(AudioChunk(samples=[0.5, -0.5, 0.3, -0.3], timestamp_ms=0))
    assert len(segments) == 1
    assert segments[0].confidence > 0.0


def test_two_chunks_different_speakers():
    vad = VADEmbeddingHandler(0.001)
    chunk1 = AudioChunk(samples=[1.0] * 10, timestamp_ms=0)
    chunk2 = AudioChunk(samples=[0.0001] * 10, timestamp_ms=100)
    segs: list[SpeakerSegment] = []
    segs = vad.handle(chunk1, segs)
    segs = vad.handle(chunk2, segs)
    assert len(segs) == 1


def test_is_speech():
    chunk = AudioChunk(vad_state=VADState.SPEECH)
    assert chunk.is_speech()
    chunk2 = AudioChunk(vad_state=VADState.SILENCE)
    assert not chunk2.is_speech()
