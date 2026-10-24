from pg_saasiso.factory import SchemaFactory
from pg_saasiso.isolator import TenantIsolator
from pg_saasiso.models import IsolationLevel, TenantConfig


def test_factory_creates_schema() -> None:
    factory = SchemaFactory()
    config = TenantConfig(tenant_id="t1", name="Acme")
    schema = factory.create_schema(config)
    assert schema.schema_name == "tenant_t1"
    assert schema.tenant_id == "t1"


def test_factory_created_count() -> None:
    factory = SchemaFactory()
    factory.create_schema(TenantConfig(tenant_id="t1", name="A"))
    factory.create_schema(TenantConfig(tenant_id="t2", name="B"))
    assert factory.created_count == 2


def test_factory_custom_schema() -> None:
    factory = SchemaFactory()
    schema = factory.create_custom_schema("t3", "Corp", ["a", "b", "c"])
    assert schema.tables == ["a", "b", "c"]


def test_isolator_provision_tenant() -> None:
    factory = SchemaFactory()
    iso = TenantIsolator(factory)
    schema = iso.provision_tenant("t1", "Acme")
    assert schema.schema_name == "tenant_t1"
    assert iso.tenant_count == 1


def test_isolator_duplicate_raises() -> None:
    factory = SchemaFactory()
    iso = TenantIsolator(factory)
    iso.provision_tenant("t1", "Acme")
    try:
        iso.provision_tenant("t1", "Acme2")
        assert False, "Should have raised"
    except ValueError:
        pass


def test_isolator_deprovision() -> None:
    factory = SchemaFactory()
    iso = TenantIsolator(factory)
    iso.provision_tenant("t1", "Acme")
    assert iso.deprovision_tenant("t1")
    assert iso.tenant_count == 0


def test_isolator_list_tenants() -> None:
    factory = SchemaFactory()
    iso = TenantIsolator(factory)
    iso.provision_tenant("t1", "A")
    iso.provision_tenant("t2", "B")
    assert iso.list_tenants() == ["t1", "t2"]


def test_isolator_get_ddl() -> None:
    factory = SchemaFactory()
    iso = TenantIsolator(factory)
    iso.provision_tenant("t1", "Acme")
    ddl = iso.get_ddl_for_tenant("t1")
    assert len(ddl) > 0
    assert "CREATE TABLE" in ddl[0]
