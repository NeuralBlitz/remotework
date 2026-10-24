from __future__ import annotations

import re
from abc import ABC, abstractmethod

from pg_search.models import SearchMode, SearchResult


class SearchStrategy(ABC):
    """Abstract search strategy."""

    @property
    @abstractmethod
    def mode(self) -> SearchMode: ...

    @abstractmethod
    def search(self, query: str, corpus: dict[str, str]) -> list[SearchResult]: ...


class FullTextStrategy(SearchStrategy):
    """Exact token matching (case-insensitive)."""

    @property
    def mode(self) -> SearchMode:
        return SearchMode.FULLTEXT

    def search(self, query: str, corpus: dict[str, str]) -> list[SearchResult]:
        tokens = set(query.lower().split())
        results: list[SearchResult] = []
        for doc_id, text in corpus.items():
            text_lower = text.lower()
            matched = [t for t in tokens if t in text_lower]
            if matched:
                score = len(matched) / max(len(tokens), 1)
                snippet = self._extract_snippet(text, matched[0])
                results.append(
                    SearchResult(doc_id=doc_id, score=score, snippet=snippet, mode=self.mode)
                )
        return sorted(results, key=lambda r: r.score, reverse=True)

    def _extract_snippet(self, text: str, token: str) -> str:
        idx = text.lower().find(token)
        if idx == -1:
            return text[:80]
        start = max(0, idx - 20)
        end = min(len(text), idx + 60)
        return text[start:end]


class FuzzyStrategy(SearchStrategy):
    """Character-level similarity matching."""

    @property
    def mode(self) -> SearchMode:
        return SearchMode.FUZZY

    def search(self, query: str, corpus: dict[str, str]) -> list[SearchResult]:
        results: list[SearchResult] = []
        query_lower = query.lower()
        for doc_id, text in corpus.items():
            words = text.lower().split()
            best_sim = 0.0
            best_word = ""
            for word in words:
                sim = self._similarity(query_lower, word)
                if sim > best_sim:
                    best_sim = sim
                    best_word = word
            if best_sim > 0.3:
                results.append(
                    SearchResult(
                        doc_id=doc_id,
                        score=best_sim,
                        snippet=f"matched: {best_word}",
                        mode=self.mode,
                    )
                )
        return sorted(results, key=lambda r: r.score, reverse=True)

    @staticmethod
    def _similarity(a: str, b: str) -> float:
        if not a or not b:
            return 0.0
        common = sum(1 for c in a if c in b)
        return common / max(len(a), len(b))


class SemanticStrategy(SearchStrategy):
    """Simulated embedding-based similarity using word overlap as proxy."""

    @property
    def mode(self) -> SearchMode:
        return SearchMode.SEMANTIC

    def search(self, query: str, corpus: dict[str, str]) -> list[SearchResult]:
        results: list[SearchResult] = []
        query_words = set(re.findall(r"\w+", query.lower()))
        for doc_id, text in corpus.items():
            doc_words = set(re.findall(r"\w+", text.lower()))
            if not query_words or not doc_words:
                continue
            intersection = query_words & doc_words
            union = query_words | doc_words
            jaccard = len(intersection) / len(union)
            if jaccard > 0:
                snippet = " ".join(list(intersection)[:5])
                results.append(
                    SearchResult(doc_id=doc_id, score=jaccard, snippet=snippet, mode=self.mode)
                )
        return sorted(results, key=lambda r: r.score, reverse=True)


class HybridStrategy(SearchStrategy):
    """Combines fulltext and semantic scores with configurable weights."""

    def __init__(self, fulltext_weight: float = 0.5, semantic_weight: float = 0.5) -> None:
        self._ft = FullTextStrategy()
        self._sem = SemanticStrategy()
        self._ft_w = fulltext_weight
        self._sem_w = semantic_weight

    @property
    def mode(self) -> SearchMode:
        return SearchMode.HYBRID

    def search(self, query: str, corpus: dict[str, str]) -> list[SearchResult]:
        ft_results = {r.doc_id: r for r in self._ft.search(query, corpus)}
        sem_results = {r.doc_id: r for r in self._sem.search(query, corpus)}
        all_ids = set(ft_results) | set(sem_results)
        combined: list[SearchResult] = []
        for doc_id in all_ids:
            ft_score = ft_results[doc_id].score if doc_id in ft_results else 0.0
            sem_score = sem_results[doc_id].score if doc_id in sem_results else 0.0
            blended = ft_score * self._ft_w + sem_score * self._sem_w
            snippet = (
                ft_results[doc_id].snippet if doc_id in ft_results else sem_results[doc_id].snippet
            )
            combined.append(
                SearchResult(doc_id=doc_id, score=blended, snippet=snippet, mode=self.mode)
            )
        return sorted(combined, key=lambda r: r.score, reverse=True)
