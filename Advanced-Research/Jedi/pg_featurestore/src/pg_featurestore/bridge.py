from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pg_featurestore.models import FeatureDefinition, FeatureValue, RetrievalMode


class StorageBackend(ABC):
    """Abstract backend that decouples feature retrieval from storage format."""

    @abstractmethod
    def store_feature(self, definition: FeatureDefinition, entity_id: str, value: Any) -> None: ...

    @abstractmethod
    def get_feature(
        self, definition: FeatureDefinition, entity_id: str, mode: RetrievalMode
    ) -> FeatureValue: ...

    @abstractmethod
    def get_features_bulk(
        self, definitions: list[FeatureDefinition], entity_ids: list[str], mode: RetrievalMode
    ) -> list[FeatureValue]: ...

    @abstractmethod
    def list_entities(self, definition: FeatureDefinition) -> list[str]: ...


class RelationalBackend(StorageBackend):
    """Simulates a traditional relational table storage (row-per-feature)."""

    def __init__(self) -> None:
        self._tables: dict[str, dict[str, Any]] = {}

    def _table_name(self, feature_name: str) -> str:
        return f"features_{feature_name}"

    def store_feature(self, definition: FeatureDefinition, entity_id: str, value: Any) -> None:
        table = self._table_name(definition.name)
        if table not in self._tables:
            self._tables[table] = {}
        self._tables[table][entity_id] = value

    def get_feature(
        self, definition: FeatureDefinition, entity_id: str, mode: RetrievalMode
    ) -> FeatureValue:
        table = self._table_name(definition.name)
        value = self._tables.get(table, {}).get(entity_id, definition.default)
        return FeatureValue(
            feature_name=definition.name,
            entity_id=entity_id,
            value=value,
            retrieved_via=mode,
        )

    def get_features_bulk(
        self, definitions: list[FeatureDefinition], entity_ids: list[str], mode: RetrievalMode
    ) -> list[FeatureValue]:
        results: list[FeatureValue] = []
        for definition in definitions:
            for eid in entity_ids:
                results.append(self.get_feature(definition, eid, mode))
        return results

    def list_entities(self, definition: FeatureDefinition) -> list[str]:
        table = self._table_name(definition.name)
        return sorted(self._tables.get(table, {}).keys())


class JSONBBackend(StorageBackend):
    """Simulates a JSONB/document storage (all features per entity in one doc)."""

    def __init__(self) -> None:
        self._store: dict[str, dict[str, Any]] = {}

    def _doc_key(self, entity_id: str) -> str:
        return f"entity:{entity_id}"

    def store_feature(self, definition: FeatureDefinition, entity_id: str, value: Any) -> None:
        key = self._doc_key(entity_id)
        if key not in self._store:
            self._store[key] = {}
        self._store[key][definition.name] = value

    def get_feature(
        self, definition: FeatureDefinition, entity_id: str, mode: RetrievalMode
    ) -> FeatureValue:
        key = self._doc_key(entity_id)
        value = self._store.get(key, {}).get(definition.name, definition.default)
        return FeatureValue(
            feature_name=definition.name,
            entity_id=entity_id,
            value=value,
            retrieved_via=mode,
        )

    def get_features_bulk(
        self, definitions: list[FeatureDefinition], entity_ids: list[str], mode: RetrievalMode
    ) -> list[FeatureValue]:
        results: list[FeatureValue] = []
        for eid in entity_ids:
            key = self._doc_key(eid)
            doc = self._store.get(key, {})
            for definition in definitions:
                value = doc.get(definition.name, definition.default)
                results.append(
                    FeatureValue(
                        feature_name=definition.name,
                        entity_id=eid,
                        value=value,
                        retrieved_via=mode,
                    )
                )
        return results

    def list_entities(self, definition: FeatureDefinition) -> list[str]:
        entity_ids: set[str] = set()
        for doc_key, doc in self._store.items():
            if definition.name in doc:
                entity_ids.add(doc_key.removeprefix("entity:"))
        return sorted(entity_ids)
