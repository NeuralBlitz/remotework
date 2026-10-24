from __future__ import annotations

from abc import ABC, abstractmethod

from pg_dbaas.models import DatabaseProfile, DatabaseTier


class DatabaseFactory(ABC):
    """Abstract factory for producing tier-appropriate database configurations."""

    @property
    @abstractmethod
    def tier(self) -> DatabaseTier: ...

    @abstractmethod
    def create_profile(self, name: str) -> DatabaseProfile: ...


class DevFactory(DatabaseFactory):
    """Small, cheap, no backups, no SSL enforcement."""

    @property
    def tier(self) -> DatabaseTier:
        return DatabaseTier.DEV

    def create_profile(self, name: str) -> DatabaseProfile:
        return DatabaseProfile(
            name=name,
            tier=self.tier,
            host="localhost",
            port=5432,
            max_connections=10,
            storage_gb=5,
            backup_enabled=False,
            ssl_required=False,
            cpu_cores=0.5,
            ram_gb=1.0,
            description="Development database",
        )


class StageFactory(DatabaseFactory):
    """Medium config with backups, SSL optional."""

    @property
    def tier(self) -> DatabaseTier:
        return DatabaseTier.STAGE

    def create_profile(self, name: str) -> DatabaseProfile:
        return DatabaseProfile(
            name=name,
            tier=self.tier,
            host="stage-db.internal",
            port=5432,
            max_connections=50,
            storage_gb=50,
            backup_enabled=True,
            ssl_required=False,
            cpu_cores=2.0,
            ram_gb=8.0,
            description="Staging database",
        )


class ProdFactory(DatabaseFactory):
    """Large config with backups, SSL mandatory."""

    @property
    def tier(self) -> DatabaseTier:
        return DatabaseTier.PROD

    def create_profile(self, name: str) -> DatabaseProfile:
        return DatabaseProfile(
            name=name,
            tier=self.tier,
            host="prod-db.internal",
            port=5432,
            max_connections=200,
            storage_gb=500,
            backup_enabled=True,
            ssl_required=True,
            cpu_cores=8.0,
            ram_gb=64.0,
            description="Production database",
        )
