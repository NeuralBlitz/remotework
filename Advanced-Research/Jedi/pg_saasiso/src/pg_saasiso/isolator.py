from __future__ import annotations

from .factory import SchemaFactory
from .models import IsolationLevel, SchemaDefinition, TenantConfig


class TenantIsolator:
    def __init__(self, factory: SchemaFactory) -> None:
        self._factory = factory
        self._tenants: dict[str, SchemaDefinition] = {}
        self._default_isolation = IsolationLevel.SCHEMA

    @property
    def tenant_count(self) -> int:
        return len(self._tenants)

    def set_default_isolation(self, level: IsolationLevel) -> None:
        self._default_isolation = level

    def provision_tenant(self, tenant_id: str, name: str) -> SchemaDefinition:
        if tenant_id in self._tenants:
            msg = f"Tenant '{tenant_id}' already provisioned"
            raise ValueError(msg)
        config = TenantConfig(tenant_id=tenant_id, name=name, isolation=self._default_isolation)
        schema = self._factory.create_schema(config)
        self._tenants[tenant_id] = schema
        return schema

    def get_tenant_schema(self, tenant_id: str) -> SchemaDefinition | None:
        return self._tenants.get(tenant_id)

    def deprovision_tenant(self, tenant_id: str) -> bool:
        if tenant_id not in self._tenants:
            return False
        del self._tenants[tenant_id]
        return True

    def list_tenants(self) -> list[str]:
        return list(self._tenants.keys())

    def get_ddl_for_tenant(self, tenant_id: str) -> list[str]:
        schema = self._tenants.get(tenant_id)
        if schema is None:
            return []
        stmts: list[str] = []
        for table in schema.tables:
            stmts.append(f"CREATE TABLE {schema.schema_name}.{table} ();")
        return stmts
