"""Tenant connection router."""

from __future__ import annotations

from typing import Any

from pg_tenancy.models import IsolationMode, TenantConfig
from pg_tenancy.strategies import (
    DatabaseIsolation,
    IsolationStrategy,
    RowIsolation,
    SchemaIsolation,
)


class TenantRouter:
    """Routes connections based on tenant isolation strategy."""

    def __init__(self) -> None:
        self._strategies: dict[IsolationMode, IsolationStrategy] = {
            IsolationMode.SCHEMA: SchemaIsolation(),
            IsolationMode.DATABASE: DatabaseIsolation(),
            IsolationMode.ROW: RowIsolation(),
        }
        self._tenants: dict[str, TenantConfig] = {}
        self._active_tenant_id: str | None = None

    def register_tenant(self, tenant: TenantConfig) -> None:
        self._tenants[tenant.tenant_id] = tenant

    def get_tenant(self, tenant_id: str) -> TenantConfig | None:
        return self._tenants.get(tenant_id)

    def get_strategy(self, mode: IsolationMode) -> IsolationStrategy:
        return self._strategies[mode]

    def set_strategy(self, mode: IsolationMode, strategy: IsolationStrategy) -> None:
        self._strategies[mode] = strategy

    def connect(self, tenant_id: str) -> dict[str, Any]:
        tenant = self._tenants.get(tenant_id)
        if tenant is None:
            raise ValueError(f"Unknown tenant: {tenant_id}")
        strategy = self._strategies[tenant.isolation_mode]
        self._active_tenant_id = tenant_id
        return strategy.apply(tenant)

    def route_query(self, tenant_id: str, query: str) -> str:
        tenant = self._tenants.get(tenant_id)
        if tenant is None:
            raise ValueError(f"Unknown tenant: {tenant_id}")
        strategy = self._strategies[tenant.isolation_mode]
        return strategy.build_query(tenant, query)

    @property
    def active_tenant_id(self) -> str | None:
        return self._active_tenant_id

    @property
    def tenant_count(self) -> int:
        return len(self._tenants)

    def list_tenants(self) -> list[str]:
        return list(self._tenants.keys())

    def disconnect(self) -> None:
        self._active_tenant_id = None
