from __future__ import annotations

from ner_engine.models import Entity
from ner_engine.pipeline import NERPipeline, PostProcessor, Tokenizer


def test_tokenizer() -> None:
    tokens = Tokenizer().tokenize("Hello World test")
    assert len(tokens) == 3
    assert tokens[0].text == "Hello"


def test_ner_extraction() -> None:
    pipeline = NERPipeline()
    entities = pipeline.run("Google is in New York")
    labels = {e.label for e in entities}
    assert "ORG" in labels
    assert "LOCATION" in labels


def test_person_detection() -> None:
    pipeline = NERPipeline()
    entities = pipeline.run("John Smith works at Microsoft")
    person = [e for e in entities if e.label == "PERSON"]
    assert len(person) == 2
    orgs = [e for e in entities if e.label == "ORG"]
    assert len(orgs) == 1


def test_post_processor_dedup() -> None:
    processor = PostProcessor()
    entities = [
        Entity(text="Google", label="ORG", start=0, end=6),
        Entity(text="Google", label="ORG", start=10, end=16),
    ]
    result = processor.process(entities)
    assert len(result) == 1


def test_empty_text() -> None:
    pipeline = NERPipeline()
    entities = pipeline.run("")
    assert entities == []
