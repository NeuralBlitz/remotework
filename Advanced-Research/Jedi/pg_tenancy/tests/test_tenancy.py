"""Tests for pg_tenancy."""

from __future__ import annotations

import pytest

from pg_tenancy.models import IsolationMode, TenantConfig
from pg_tenancy.router import TenantRouter
from pg_tenancy.strategies import DatabaseIsolation, RowIsolation, SchemaIsolation


class TestTenantConfig:
    def test_defaults(self) -> None:
        t = TenantConfig(tenant_id="acme", name="Acme Corp")
        assert t.schema_name == "tenant_acme"
        assert t.database_name == "db_tenant_acme"
        assert t.isolation_mode == IsolationMode.SCHEMA

    def test_has_connection(self) -> None:
        t = TenantConfig(tenant_id="1", name="T", connection_string="pg://localhost/db")
        assert t.has_connection

    def test_qualified_schema(self) -> None:
        t = TenantConfig(tenant_id="1", name="T")
        assert "tenant_1" in t.qualified_schema


class TestSchemaIsolation:
    def test_apply(self) -> None:
        strategy = SchemaIsolation()
        tenant = TenantConfig(tenant_id="t1", name="Tenant 1")
        result = strategy.apply(tenant)
        assert "search_path" in result
        assert result["search_path"] == "tenant_t1"

    def test_build_query(self) -> None:
        strategy = SchemaIsolation()
        tenant = TenantConfig(tenant_id="t1", name="T")
        q = strategy.build_query(tenant, "SELECT 1")
        assert "SET search_path" in q
        assert "SELECT 1" in q

    def test_name(self) -> None:
        assert SchemaIsolation().strategy_name == "schema_isolation"


class TestDatabaseIsolation:
    def test_apply(self) -> None:
        strategy = DatabaseIsolation()
        tenant = TenantConfig(tenant_id="t1", name="T")
        result = strategy.apply(tenant)
        assert result["database"] == "db_tenant_t1"
        assert any("CREATE DATABASE" in c for c in result["commands"])

    def test_build_query(self) -> None:
        strategy = DatabaseIsolation()
        tenant = TenantConfig(tenant_id="t1", name="T")
        q = strategy.build_query(tenant, "SELECT * FROM users")
        assert "\\c" in q
        assert "SELECT * FROM users" in q


class TestRowIsolation:
    def test_apply(self) -> None:
        strategy = RowIsolation()
        tenant = TenantConfig(tenant_id="t1", name="T")
        result = strategy.apply(tenant)
        assert result["rls_enabled"]
        assert any("app.current_tenant" in c for c in result["commands"])

    def test_build_query(self) -> None:
        strategy = RowIsolation()
        tenant = TenantConfig(tenant_id="t1", name="T")
        q = strategy.build_query(tenant, "SELECT 1")
        assert "app.current_tenant" in q
        assert "SELECT 1" in q


class TestTenantRouter:
    def test_register_and_get(self) -> None:
        router = TenantRouter()
        tenant = TenantConfig(tenant_id="acme", name="Acme")
        router.register_tenant(tenant)
        assert router.tenant_count == 1
        assert router.get_tenant("acme") is tenant

    def test_connect_schema(self) -> None:
        router = TenantRouter()
        router.register_tenant(TenantConfig(tenant_id="t1", name="T1"))
        result = router.connect("t1")
        assert "search_path" in result
        assert router.active_tenant_id == "t1"

    def test_connect_database(self) -> None:
        router = TenantRouter()
        router.register_tenant(
            TenantConfig(tenant_id="t2", name="T2", isolation_mode=IsolationMode.DATABASE)
        )
        result = router.connect("t2")
        assert "database" in result

    def test_connect_row(self) -> None:
        router = TenantRouter()
        router.register_tenant(
            TenantConfig(tenant_id="t3", name="T3", isolation_mode=IsolationMode.ROW)
        )
        result = router.connect("t3")
        assert result["rls_enabled"]

    def test_connect_unknown_raises(self) -> None:
        router = TenantRouter()
        with pytest.raises(ValueError, match="Unknown tenant"):
            router.connect("nonexistent")

    def test_route_query(self) -> None:
        router = TenantRouter()
        router.register_tenant(TenantConfig(tenant_id="t1", name="T1"))
        q = router.route_query("t1", "SELECT 1")
        assert "SELECT 1" in q

    def test_disconnect(self) -> None:
        router = TenantRouter()
        router.register_tenant(TenantConfig(tenant_id="t1", name="T1"))
        router.connect("t1")
        router.disconnect()
        assert router.active_tenant_id is None

    def test_list_tenants(self) -> None:
        router = TenantRouter()
        router.register_tenant(TenantConfig(tenant_id="a", name="A"))
        router.register_tenant(TenantConfig(tenant_id="b", name="B"))
        assert sorted(router.list_tenants()) == ["a", "b"]
