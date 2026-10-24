from __future__ import annotations

from abc import ABC, abstractmethod

from .models import Document, Query, Score


class RankingStrategy(ABC):
    @abstractmethod
    def rank(self, query: Query, documents: list[Document]) -> list[Score]:
        raise NotImplementedError


class BM25Ranker(RankingStrategy):
    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b

    def rank(self, query: Query, documents: list[Document]) -> list[Score]:
        scores: list[Score] = []
        avg_dl = sum(len(d.content.split()) for d in documents) / max(len(documents), 1)
        terms = query.text.lower().split()
        for doc in documents:
            words = doc.content.lower().split()
            dl = len(words)
            tf_sum = 0.0
            for term in terms:
                tf = words.count(term)
                denom = tf + self.k1 * (1 - self.b + self.b * dl / max(avg_dl, 1))
                tf_sum += (tf * (self.k1 + 1)) / denom
            scores.append(Score(document_id=doc.document_id, value=tf_sum))
        scores.sort(key=lambda s: s.value, reverse=True)
        return scores


class NeuralRanker(RankingStrategy):
    def rank(self, query: Query, documents: list[Document]) -> list[Score]:
        scores: list[Score] = []
        q_terms = set(query.text.lower().split())
        for doc in documents:
            d_terms = set(doc.content.lower().split())
            overlap = len(q_terms & d_terms) / max(len(q_terms | d_terms), 1)
            scores.append(Score(document_id=doc.document_id, value=overlap))
        scores.sort(key=lambda s: s.value, reverse=True)
        return scores


class HybridRanker(RankingStrategy):
    def __init__(self) -> None:
        self._bm25 = BM25Ranker()
        self._neural = NeuralRanker()

    def rank(self, query: Query, documents: list[Document]) -> list[Score]:
        bm25_scores = {s.document_id: s.value for s in self._bm25.rank(query, documents)}
        neural_scores = {s.document_id: s.value for s in self._neural.rank(query, documents)}
        combined: list[Score] = []
        for doc in documents:
            b = bm25_scores.get(doc.document_id, 0.0)
            n = neural_scores.get(doc.document_id, 0.0)
            combined.append(Score(document_id=doc.document_id, value=0.5 * b + 0.5 * n))
        combined.sort(key=lambda s: s.value, reverse=True)
        return combined
