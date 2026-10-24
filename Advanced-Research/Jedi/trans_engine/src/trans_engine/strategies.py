from __future__ import annotations

from abc import ABC, abstractmethod

from .models import TranslationRequest, TranslationResult


class TranslationStrategy(ABC):
    @abstractmethod
    def translate(self, request: TranslationRequest) -> TranslationResult:
        raise NotImplementedError


class RuleTranslation(TranslationStrategy):
    DICTIONARIES: dict[str, dict[str, str]] = {
        "es": {"hello": "hola", "world": "mundo", "good": "bueno", "morning": "manana"},
        "fr": {"hello": "bonjour", "world": "monde", "good": "bon", "morning": "matin"},
        "de": {"hello": "hallo", "world": "welt", "good": "gut", "morning": "morgen"},
    }

    def translate(self, request: TranslationRequest) -> TranslationResult:
        dictionary = self.DICTIONARIES.get(request.target_language, {})
        words = request.text.lower().split()
        translated = [dictionary.get(w, w) for w in words]
        return TranslationResult(
            request_id=request.request_id,
            translated_text=" ".join(translated),
            source_language=request.source_language,
            target_language=request.target_language,
        )


class NeuralTranslation(TranslationStrategy):
    def translate(self, request: TranslationRequest) -> TranslationResult:
        prefix = f"[{request.target_language}]"
        return TranslationResult(
            request_id=request.request_id,
            translated_text=f"{prefix} {request.text}",
            source_language=request.source_language,
            target_language=request.target_language,
        )

