from __future__ import annotations

from search_rank.models import Document, Query
from search_rank.strategies import BM25Ranker, HybridRanker, NeuralRanker


def _make_docs() -> tuple[Query, list[Document]]:
    query = Query(text="python programming")
    docs = [
        Document(document_id="d1", content="python is a programming language"),
        Document(document_id="d2", content="java is also programming"),
        Document(document_id="d3", content="cooking recipes"),
    ]
    return query, docs


def test_bm25_ranking() -> None:
    query, docs = _make_docs()
    ranker = BM25Ranker()
    scores = ranker.rank(query, docs)
    assert len(scores) == 3
    assert scores[0].value >= scores[-1].value


def test_neural_ranking() -> None:
    query, docs = _make_docs()
    ranker = NeuralRanker()
    scores = ranker.rank(query, docs)
    assert len(scores) == 3


def test_hybrid_ranking() -> None:
    query, docs = _make_docs()
    ranker = HybridRanker()
    scores = ranker.rank(query, docs)
    assert len(scores) == 3


def test_bm25_relevant_first() -> None:
    query, docs = _make_docs()
    ranker = BM25Ranker()
    scores = ranker.rank(query, docs)
    assert scores[0].document_id == "d1"


def test_empty_documents() -> None:
    query = Query(text="test")
    ranker = BM25Ranker()
    scores = ranker.rank(query, [])
    assert scores == []

