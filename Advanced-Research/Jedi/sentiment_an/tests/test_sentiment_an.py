from __future__ import annotations

from sentiment_an.models import SentimentResult, Text
from sentiment_an.strategies import LLMSentiment, MLSentiment, RuleSentiment


def test_rule_positive() -> None:
    strategy = RuleSentiment()
    result = strategy.analyze(Text(content="This is great and wonderful"))
    assert result.label == "positive"


def test_rule_negative() -> None:
    strategy = RuleSentiment()
    result = strategy.analyze(Text(content="This is terrible and awful"))
    assert result.label == "negative"


def test_ml_sentiment() -> None:
    strategy = MLSentiment()
    result = strategy.analyze(Text(content="I love this good product"))
    assert result.label == "positive"


def test_llm_neutral() -> None:
    strategy = LLMSentiment()
    result = strategy.analyze(Text(content="The weather is cloudy today"))
    assert result.label == "neutral"


def test_all_strategies_consistent() -> None:
    text = Text(content="This is great")
    for strategy in [RuleSentiment(), MLSentiment(), LLMSentiment()]:
        result = strategy.analyze(text)
        assert isinstance(result, SentimentResult)

