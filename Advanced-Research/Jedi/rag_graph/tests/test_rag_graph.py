from rag_graph.bridge import InMemoryBackend
from rag_graph.models import Subgraph, Triplet
from rag_graph.retriever import SubgraphRetriever, TripletRetriever


def _make_backend() -> InMemoryBackend:
    b = InMemoryBackend()
    b.add_triplet(Triplet("Alice", "knows", "Bob"))
    b.add_triplet(Triplet("Bob", "works_at", "Acme"))
    b.add_triplet(Triplet("Alice", "likes", "Python"))
    return b


def test_inmemory_add_and_count() -> None:
    b = _make_backend()
    assert b.count() == 3


def test_get_by_head() -> None:
    b = _make_backend()
    results = b.get_by_head("Alice")
    assert len(results) == 2


def test_get_by_relation() -> None:
    b = _make_backend()
    results = b.get_by_relation("knows")
    assert len(results) == 1
    assert results[0].tail == "Bob"


def test_get_neighbors() -> None:
    b = _make_backend()
    neighbors = b.get_neighbors("Bob")
    assert len(neighbors) == 2


def test_triplet_retriever() -> None:
    b = _make_backend()
    r = TripletRetriever(b)
    results = r.retrieve_by_head("Alice")
    assert len(results) == 2


def test_subgraph_retriever_ego() -> None:
    b = _make_backend()
    r = SubgraphRetriever(b)
    sg = r.retrieve_ego("Alice", hops=2)
    assert sg.size >= 2
    assert "Alice" in sg.entities


def test_subgraph_properties() -> None:
    sg = Subgraph()
    sg.add_triplet(Triplet("A", "rel", "B"))
    assert sg.size == 1
    assert "A" in sg.entities
    assert "B" in sg.entities


def test_subgraph_empty() -> None:
    sg = Subgraph()
    assert sg.size == 0
    assert len(sg.entities) == 0


def test_triplet_score_default() -> None:
    t = Triplet("X", "rel", "Y")
    assert t.score == 1.0


def test_backend_empty_count() -> None:
    b = InMemoryBackend()
    assert b.count() == 0
