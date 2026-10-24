from __future__ import annotations

from trans_engine.models import TranslationRequest
from trans_engine.strategies import NeuralTranslation, RuleTranslation


def test_rule_translation() -> None:
    strategy = RuleTranslation()
    req = TranslationRequest(request_id="r1", text="hello world", target_language="es")
    result = strategy.translate(req)
    assert "hola" in result.translated_text


def test_neural_translation() -> None:
    strategy = NeuralTranslation()
    req = TranslationRequest(request_id="r2", text="hello", target_language="fr")
    result = strategy.translate(req)
    assert result.translated_text.startswith("[fr]")


def test_unknown_words_unchanged() -> None:
    strategy = RuleTranslation()
    req = TranslationRequest(request_id="r3", text="python is awesome", target_language="es")
    result = strategy.translate(req)
    assert "python" in result.translated_text


def test_multiple_languages() -> None:
    strategy = RuleTranslation()
    for lang in ("es", "fr", "de"):
        req = TranslationRequest(request_id="r", text="hello", target_language=lang)
        result = strategy.translate(req)
        assert result.target_language == lang


def test_preserves_request_id() -> None:
    strategy = NeuralTranslation()
    req = TranslationRequest(request_id="unique-id", text="test")
    result = strategy.translate(req)
    assert result.request_id == "unique-id"

