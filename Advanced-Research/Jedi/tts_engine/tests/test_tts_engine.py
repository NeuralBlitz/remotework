from __future__ import annotations

from tts_engine.models import TextRequest
from tts_engine.pipeline import PhonemeConverter, TextNormalizer, TTSPipeline


def test_normalizer() -> None:
    normalizer = TextNormalizer()
    assert "Mister" in normalizer.normalize("Hello Mr. Smith")


def test_phoneme_converter() -> None:
    converter = PhonemeConverter()
    phonemes = converter.convert("hi")
    assert len(phonemes) == 2
    assert phonemes[0].startswith("C")


def test_pipeline() -> None:
    pipeline = TTSPipeline()
    req = TextRequest(text="Hello world")
    output = pipeline.run(req)
    assert output.duration_ms > 0
    assert output.phoneme_count > 0


def test_empty_text() -> None:
    pipeline = TTSPipeline()
    req = TextRequest(text="")
    output = pipeline.run(req)
    assert output.duration_ms == 0


def test_custom_sample_rate() -> None:
    pipeline = TTSPipeline(sample_rate=44100)
    req = TextRequest(text="test")
    output = pipeline.run(req)
    assert output.sample_rate == 44100

