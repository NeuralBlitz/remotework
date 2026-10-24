
from pg_featurestore.bridge import JSONBBackend, RelationalBackend
from pg_featurestore.models import FeatureDefinition, RetrievalMode
from pg_featurestore.store import FeatureStore


def _make_store(backend: str = "relational") -> tuple[FeatureStore, list[FeatureDefinition]]:
    if backend == "jsonb":
        store = FeatureStore(JSONBBackend())
    else:
        store = FeatureStore(RelationalBackend())
    age_def = FeatureDefinition(name="age", entity_key="user_id", description="User age")
    score_def = FeatureDefinition(name="score", entity_key="user_id", default=0.0)
    store.register_feature(age_def)
    store.register_feature(score_def)
    return store, [age_def, score_def]


class TestFeatureDefinition:
    def test_default_values(self) -> None:
        fd = FeatureDefinition(name="x", entity_key="eid")
        assert fd.description == ""
        assert fd.default is None

    def test_frozen(self) -> None:
        fd = FeatureDefinition(name="x", entity_key="eid")
        try:
            fd.name = "y"  # type: ignore[misc]
            assert False, "Should be frozen"
        except AttributeError:
            pass


class TestRelationalBackend:
    def test_store_and_retrieve(self) -> None:
        store, defs = _make_store("relational")
        store.ingest("age", "u1", 30)
        val = store.get("age", "u1")
        assert val.value == 30
        assert val.entity_id == "u1"

    def test_default_when_missing(self) -> None:
        store, _ = _make_store("relational")
        val = store.get("score", "unknown")
        assert val.value == 0.0

    def test_bulk_retrieve(self) -> None:
        store, _ = _make_store("relational")
        store.ingest("age", "u1", 25)
        store.ingest("score", "u1", 99.5)
        results = store.get_multi(["age", "score"], ["u1"])
        assert len(results) == 2

    def test_list_entities(self) -> None:
        store, _ = _make_store("relational")
        store.ingest("age", "u2", 40)
        store.ingest("age", "u1", 30)
        assert store.list_entities("age") == ["u1", "u2"]


class TestJSONBBackend:
    def test_store_and_retrieve(self) -> None:
        store, _ = _make_store("jsonb")
        store.ingest("age", "u1", 30)
        val = store.get("age", "u1", mode=RetrievalMode.OFFLINE)
        assert val.value == 30
        assert val.retrieved_via == RetrievalMode.OFFLINE

    def test_default_when_missing(self) -> None:
        store, _ = _make_store("jsonb")
        val = store.get("score", "nobody")
        assert val.value == 0.0

    def test_bulk_retrieve(self) -> None:
        store, _ = _make_store("jsonb")
        store.ingest("age", "u1", 25)
        store.ingest("age", "u2", 35)
        results = store.get_multi(["age"], ["u1", "u2"])
        assert len(results) == 2


class TestFeatureStore:
    def test_registered_features(self) -> None:
        store, _ = _make_store()
        assert store.registered_features == ["age", "score"]

    def test_get_definition(self) -> None:
        store, defs = _make_store()
        assert store.get_definition("age") is defs[0]

    def test_both_backends_produce_same_values(self) -> None:
        rel_store, _ = _make_store("relational")
        jsonb_store, _ = _make_store("jsonb")
        rel_store.ingest("age", "u1", 42)
        jsonb_store.ingest("age", "u1", 42)
        assert rel_store.get("age", "u1").value == jsonb_store.get("age", "u1").value
