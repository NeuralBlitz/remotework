from __future__ import annotations

from typing import Any

from pg_featurestore.bridge import StorageBackend
from pg_featurestore.models import FeatureDefinition, FeatureValue, RetrievalMode


class FeatureStore:
    """High-level feature store that retrieves features via a pluggable backend."""

    def __init__(self, backend: StorageBackend) -> None:
        self._backend = backend
        self._definitions: dict[str, FeatureDefinition] = {}

    def register_feature(self, definition: FeatureDefinition) -> None:
        self._definitions[definition.name] = definition

    def get_definition(self, name: str) -> FeatureDefinition | None:
        return self._definitions.get(name)

    def ingest(self, feature_name: str, entity_id: str, value: Any) -> None:
        definition = self._definitions[feature_name]
        self._backend.store_feature(definition, entity_id, value)

    def get(
        self, feature_name: str, entity_id: str, mode: RetrievalMode = RetrievalMode.ONLINE
    ) -> FeatureValue:
        definition = self._definitions[feature_name]
        return self._backend.get_feature(definition, entity_id, mode)

    def get_multi(
        self,
        feature_names: list[str],
        entity_ids: list[str],
        mode: RetrievalMode = RetrievalMode.ONLINE,
    ) -> list[FeatureValue]:
        definitions = [self._definitions[name] for name in feature_names]
        return self._backend.get_features_bulk(definitions, entity_ids, mode)

    def list_entities(self, feature_name: str) -> list[str]:
        definition = self._definitions[feature_name]
        return self._backend.list_entities(definition)

    @property
    def registered_features(self) -> list[str]:
        return sorted(self._definitions.keys())
