from __future__ import annotations

from summarizer.models import Document
from summarizer.strategies import AbstractiveSummarizer, ExtractiveSummarizer


def _make_doc() -> Document:
    return Document(
        document_id="d1",
        title="Test",
        content="Python is great. Machine learning is powerful. Data science is useful.",
    )


def test_extractive_summary() -> None:
    strategy = ExtractiveSummarizer()
    summary = strategy.summarize(_make_doc(), max_sentences=2)
    assert summary.document_id == "d1"
    assert len(summary.text) > 0


def test_abstractive_summary() -> None:
    strategy = AbstractiveSummarizer()
    summary = strategy.summarize(_make_doc(), max_sentences=2)
    assert summary.document_id == "d1"
    assert len(summary.text) > 0


def test_empty_document() -> None:
    doc = Document(document_id="d2", content="")
    summary = ExtractiveSummarizer().summarize(doc)
    assert summary.text == ""


def test_max_sentences_respected() -> None:
    strategy = ExtractiveSummarizer()
    doc = Document(document_id="d3", content="A. B. C. D. E.")
    summary = strategy.summarize(doc, max_sentences=2)
    assert summary.text.count(".") <= 3


def test_summary_preserves_doc_id() -> None:
    doc = Document(document_id="custom-id", content="Some text here.")
    summary = ExtractiveSummarizer().summarize(doc)
    assert summary.document_id == "custom-id"

