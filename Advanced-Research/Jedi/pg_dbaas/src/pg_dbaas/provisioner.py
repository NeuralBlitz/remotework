from __future__ import annotations

from pg_dbaas.factory import DatabaseFactory, DevFactory, ProdFactory, StageFactory
from pg_dbaas.models import DatabaseProfile, DatabaseTier


class Provisioner:
    """Creates databases with tier-appropriate configuration."""

    _FACTORIES: dict[DatabaseTier, type[DatabaseFactory]] = {
        DatabaseTier.DEV: DevFactory,
        DatabaseTier.STAGE: StageFactory,
        DatabaseTier.PROD: ProdFactory,
    }

    def __init__(self) -> None:
        self._provisioned: dict[str, DatabaseProfile] = {}
        self._custom_factories: dict[DatabaseTier, DatabaseFactory] = {}

    def register_factory(self, tier: DatabaseTier, factory: DatabaseFactory) -> None:
        self._custom_factories[tier] = factory

    def _get_factory(self, tier: DatabaseTier) -> DatabaseFactory:
        if tier in self._custom_factories:
            return self._custom_factories[tier]
        cls = self._FACTORIES.get(tier)
        if cls is None:
            raise ValueError(f"No factory registered for tier: {tier}")
        return cls()

    def provision(self, name: str, tier: DatabaseTier) -> DatabaseProfile:
        if name in self._provisioned:
            raise ValueError(f"Database '{name}' already provisioned")
        factory = self._get_factory(tier)
        profile = factory.create_profile(name)
        self._provisioned[name] = profile
        return profile

    def get_profile(self, name: str) -> DatabaseProfile | None:
        return self._provisioned.get(name)

    def list_provisioned(self) -> list[str]:
        return sorted(self._provisioned.keys())

    def deprovision(self, name: str) -> DatabaseProfile:
        if name not in self._provisioned:
            raise KeyError(f"Database '{name}' not found")
        return self._provisioned.pop(name)

    @property
    def count(self) -> int:
        return len(self._provisioned)
