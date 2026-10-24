from __future__ import annotations

from topic_model.models import Document
from topic_model.pipeline import LDAModel, Preprocessor, TopicPipeline


def _make_docs() -> list[Document]:
    return [
        Document(document_id="d1", content="Python is a programming language for software"),
        Document(document_id="d2", content="Machine learning uses data for predictions"),
        Document(document_id="d3", content="Web development with Python and JavaScript"),
    ]


def test_preprocessor() -> None:
    doc = Document(document_id="d1", content="The cat is on the mat")
    tokens = Preprocessor().process(doc)
    assert "the" not in tokens
    assert "cat" in tokens


def test_pipeline_returns_topics() -> None:
    pipeline = TopicPipeline(num_topics=2)
    topics = pipeline.run(_make_docs())
    assert len(topics) == 2


def test_topic_has_keywords() -> None:
    pipeline = TopicPipeline(num_topics=2)
    topics = pipeline.run(_make_docs())
    for topic in topics:
        assert len(topic.keywords) > 0


def test_lda_model() -> None:
    model = LDAModel(num_topics=2)
    tokenized = [["python", "code"], ["data", "learn"]]
    topics = model.fit(tokenized)
    assert len(topics) == 2


def test_empty_documents() -> None:
    pipeline = TopicPipeline(num_topics=1)
    topics = pipeline.run([])
    assert len(topics) == 1

