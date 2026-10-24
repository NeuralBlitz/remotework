from __future__ import annotations

from abc import ABC, abstractmethod

from .models import SentimentResult, Text


class SentimentStrategy(ABC):
    @abstractmethod
    def analyze(self, text: Text) -> SentimentResult:
        raise NotImplementedError


class RuleSentiment(SentimentStrategy):
    POSITIVE = {"good", "great", "excellent", "amazing", "love", "happy", "wonderful"}
    NEGATIVE = {"bad", "terrible", "awful", "hate", "sad", "horrible", "worst"}

    def analyze(self, text: Text) -> SentimentResult:
        words = set(text.content.lower().split())
        pos = len(words & self.POSITIVE)
        neg = len(words & self.NEGATIVE)
        total = pos + neg
        if total == 0:
            return SentimentResult(label="neutral", score=0.0)
        score = (pos - neg) / total
        label = "positive" if score > 0 else "negative" if score < 0 else "neutral"
        return SentimentResult(label=label, score=score)


class MLSentiment(SentimentStrategy):
    def __init__(self) -> None:
        self._weights: dict[str, float] = {
            "good": 0.8, "great": 0.9, "bad": -0.7, "terrible": -0.9,
            "love": 0.85, "hate": -0.85, "okay": 0.1,
        }

    def analyze(self, text: Text) -> SentimentResult:
        words = text.content.lower().split()
        scores = [self._weights.get(w, 0.0) for w in words]
        avg = sum(scores) / max(len(scores), 1)
        label = "positive" if avg > 0.1 else "negative" if avg < -0.1 else "neutral"
        return SentimentResult(label=label, score=avg)


class LLMSentiment(SentimentStrategy):
    def analyze(self, text: Text) -> SentimentResult:
        words = text.content.lower().split()
        sentiment_words = {"good", "great", "bad", "terrible", "love", "hate"}
        relevant = [w for w in words if w in sentiment_words]
        if not relevant:
            return SentimentResult(label="neutral", score=0.0)
        pos = sum(1 for w in relevant if w in {"good", "great", "love"})
        neg = sum(1 for w in relevant if w in {"bad", "terrible", "hate"})
        score = (pos - neg) / len(relevant)
        label = "positive" if score > 0 else "negative" if score < 0 else "neutral"
        return SentimentResult(label=label, score=score)

