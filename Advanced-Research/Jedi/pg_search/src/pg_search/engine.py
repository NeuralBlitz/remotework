from __future__ import annotations

from pg_search.models import SearchMode, SearchResult
from pg_search.strategies import (
    FullTextStrategy,
    FuzzyStrategy,
    HybridStrategy,
    SearchStrategy,
    SemanticStrategy,
)


class SearchEngine:
    """Selects and executes a search strategy dynamically."""

    _STRATEGY_MAP: dict[SearchMode, type[SearchStrategy]] = {
        SearchMode.FULLTEXT: FullTextStrategy,
        SearchMode.FUZZY: FuzzyStrategy,
        SearchMode.SEMANTIC: SemanticStrategy,
        SearchMode.HYBRID: HybridStrategy,
    }

    def __init__(self, default_mode: SearchMode = SearchMode.FULLTEXT) -> None:
        self._default_mode = default_mode
        self._corpus: dict[str, str] = {}
        self._custom_strategies: dict[SearchMode, SearchStrategy] = {}

    def index_document(self, doc_id: str, text: str) -> None:
        self._corpus[doc_id] = text

    def index_bulk(self, documents: dict[str, str]) -> None:
        self._corpus.update(documents)

    def register_strategy(self, mode: SearchMode, strategy: SearchStrategy) -> None:
        self._custom_strategies[mode] = strategy

    def _get_strategy(self, mode: SearchMode | None) -> SearchStrategy:
        resolved = mode or self._default_mode
        if resolved in self._custom_strategies:
            return self._custom_strategies[resolved]
        cls = self._STRATEGY_MAP.get(resolved)
        if cls is None:
            raise ValueError(f"Unknown search mode: {resolved}")
        return cls()

    def search(
        self, query: str, mode: SearchMode | None = None, top_k: int = 10
    ) -> list[SearchResult]:
        strategy = self._get_strategy(mode)
        results = strategy.search(query, self._corpus)
        return results[:top_k]

    @property
    def corpus_size(self) -> int:
        return len(self._corpus)
