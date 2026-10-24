from pg_search.engine import SearchEngine
from pg_search.models import SearchMode, SearchResult
from pg_search.strategies import FullTextStrategy, FuzzyStrategy, HybridStrategy, SemanticStrategy

CORPUS: dict[str, str] = {
    "d1": "PostgreSQL is a powerful open source database",
    "d2": "Python is great for data science and machine learning",
    "d3": "Docker containers simplify application deployment",
    "d4": "pgvector enables semantic search in PostgreSQL",
}


class TestFullTextStrategy:
    def test_exact_match(self) -> None:
        s = FullTextStrategy()
        results = s.search("PostgreSQL", CORPUS)
        assert len(results) >= 2
        assert all(r.doc_id in ("d1", "d4") for r in results[:2])

    def test_no_match(self) -> None:
        s = FullTextStrategy()
        results = s.search("xyzzy", CORPUS)
        assert len(results) == 0

    def test_case_insensitive(self) -> None:
        s = FullTextStrategy()
        results = s.search("python", CORPUS)
        assert any(r.doc_id == "d2" for r in results)


class TestFuzzyStrategy:
    def test_finds_similar(self) -> None:
        s = FuzzyStrategy()
        results = s.search("PostgrSQL", CORPUS)  # typo
        assert len(results) > 0

    def test_mode_is_fuzzy(self) -> None:
        s = FuzzyStrategy()
        assert s.mode == SearchMode.FUZZY


class TestSemanticStrategy:
    def test_jaccard_match(self) -> None:
        s = SemanticStrategy()
        results = s.search("database search vector", CORPUS)
        assert len(results) > 0
        assert results[0].score > 0

    def test_mode_is_semantic(self) -> None:
        s = SemanticStrategy()
        assert s.mode == SearchMode.SEMANTIC


class TestHybridStrategy:
    def test_combines_scores(self) -> None:
        s = HybridStrategy()
        results = s.search("PostgreSQL", CORPUS)
        assert len(results) > 0
        assert all(r.mode == SearchMode.HYBRID for r in results)

    def test_custom_weights(self) -> None:
        s = HybridStrategy(fulltext_weight=0.8, semantic_weight=0.2)
        results = s.search("database", CORPUS)
        assert len(results) > 0


class TestSearchEngine:
    def test_default_mode(self) -> None:
        engine = SearchEngine(default_mode=SearchMode.FULLTEXT)
        engine.index_bulk(CORPUS)
        results = engine.search("Python")
        assert len(results) > 0

    def test_override_mode(self) -> None:
        engine = SearchEngine()
        engine.index_bulk(CORPUS)
        results = engine.search("Docker", mode=SearchMode.FUZZY)
        assert len(results) > 0

    def test_top_k(self) -> None:
        engine = SearchEngine()
        engine.index_bulk(CORPUS)
        results = engine.search("PostgreSQL", top_k=1)
        assert len(results) == 1

    def test_corpus_size(self) -> None:
        engine = SearchEngine()
        engine.index_bulk(CORPUS)
        assert engine.corpus_size == 4

    def test_register_custom_strategy(self) -> None:
        class AlwaysFirst(FullTextStrategy):
            def search(self, query: str, corpus: dict[str, str]) -> list[SearchResult]:
                return [SearchResult(doc_id="d1", score=1.0, mode=self.mode)]

        engine = SearchEngine()
        engine.index_bulk(CORPUS)
        engine.register_strategy(SearchMode.FULLTEXT, AlwaysFirst())
        results = engine.search("xyz", mode=SearchMode.FULLTEXT)
        assert results[0].doc_id == "d1"
