"""Tenant isolation strategies."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pg_tenancy.models import TenantConfig


class IsolationStrategy(ABC):
    """Base class for tenant isolation strategies."""

    @abstractmethod
    def apply(self, tenant: TenantConfig) -> dict[str, Any]: ...

    @abstractmethod
    def build_query(self, tenant: TenantConfig, base_query: str) -> str: ...

    @property
    @abstractmethod
    def strategy_name(self) -> str: ...


class SchemaIsolation(IsolationStrategy):
    """Isolates tenants using PostgreSQL schemas."""

    def apply(self, tenant: TenantConfig) -> dict[str, Any]:
        return {
            "search_path": tenant.schema_name,
            "commands": [
                f"CREATE SCHEMA IF NOT EXISTS {tenant.schema_name}",
                f"SET search_path TO {tenant.schema_name}",
            ],
        }

    def build_query(self, tenant: TenantConfig, base_query: str) -> str:
        return f"SET search_path TO {tenant.schema_name}; {base_query}"

    @property
    def strategy_name(self) -> str:
        return "schema_isolation"


class DatabaseIsolation(IsolationStrategy):
    """Isolates tenants using separate databases."""

    def apply(self, tenant: TenantConfig) -> dict[str, Any]:
        return {
            "database": tenant.database_name,
            "commands": [
                f"CREATE DATABASE {tenant.database_name}",
                f"\\c {tenant.database_name}",
                f"CREATE SCHEMA IF NOT EXISTS {tenant.schema_name}",
            ],
        }

    def build_query(self, tenant: TenantConfig, base_query: str) -> str:
        return f"\\c {tenant.database_name}; SET search_path TO {tenant.schema_name}; {base_query}"

    @property
    def strategy_name(self) -> str:
        return "database_isolation"


class RowIsolation(IsolationStrategy):
    """Isolates tenants using Row-Level Security policies."""

    def apply(self, tenant: TenantConfig) -> dict[str, Any]:
        policy = tenant.rls_policy or f"tenant_id = '{tenant.tenant_id}'"
        return {
            "rls_enabled": True,
            "commands": [
                "ALTER TABLE shared_data ENABLE ROW LEVEL SECURITY",
                f"CREATE POLICY tenant_policy_{tenant.tenant_id} ON shared_data USING ({policy})",
                f"SET app.current_tenant = '{tenant.tenant_id}'",
            ],
        }

    def build_query(self, tenant: TenantConfig, base_query: str) -> str:
        return f"SET app.current_tenant = '{tenant.tenant_id}'; {base_query}"

    @property
    def strategy_name(self) -> str:
        return "row_isolation"
