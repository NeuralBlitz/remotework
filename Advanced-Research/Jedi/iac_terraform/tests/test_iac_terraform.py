import pytest
from iac_terraform.models import TerraformResource, PGInstance, ResourceProvider
from iac_terraform.generator import TerraformGenerator
from iac_terraform.modules import PGModule, NetworkModule


def test_terraform_resource_creation() -> None:
    r = TerraformResource(
        resource_type="aws_db_instance", name="main", provider=ResourceProvider.AWS
    )
    assert r.name == "main"
    assert r.provider == ResourceProvider.AWS


def test_terraform_resource_to_hcl() -> None:
    r = TerraformResource(
        resource_type="aws_db_instance",
        name="pg",
        provider=ResourceProvider.AWS,
        properties={"engine": "postgres", "allocated_storage": 100},
    )
    hcl = r.to_hcl()
    assert "aws_db_instance" in hcl
    assert "postgres" in hcl


def test_pginstance_creation() -> None:
    pg = PGInstance(name="main-pg", instance_class="db.t3.medium", storage_gb=100)
    assert pg.engine_version == "16.2"
    assert pg.multi_az is True


def test_pginstance_to_resource() -> None:
    pg = PGInstance(name="test", instance_class="db.t3.small", storage_gb=50)
    resource = pg.to_resource()
    assert resource.resource_type == "aws_db_instance"
    assert resource.properties["allocated_storage"] == 50


def test_generator_add_instance() -> None:
    gen = TerraformGenerator(provider=ResourceProvider.AWS, region="us-east-1")
    pg = PGInstance(name="main", instance_class="db.t3.medium", storage_gb=200)
    gen.add_pg_instance(pg)
    assert gen.resource_count == 1


def test_generator_add_variable() -> None:
    gen = TerraformGenerator(provider=ResourceProvider.AWS, region="us-west-2")
    gen.add_variable("db_password", "Database password")
    assert gen.variable_count == 1


def test_generator_generate() -> None:
    gen = TerraformGenerator(provider=ResourceProvider.AWS, region="us-east-1")
    gen.add_variable("region", "AWS region")
    gen.add_output("db_endpoint", "aws_db_instance.main.endpoint")
    hcl = gen.generate()
    assert "provider" in hcl
    assert "variable" in hcl
    assert "output" in hcl


def test_pg_module_hcl() -> None:
    m = PGModule(name="pg-cluster", instance_class="db.r5.large", storage_gb=500)
    hcl = m.to_hcl()
    assert "module" in hcl
    assert "db.r5.large" in hcl


def test_pg_module_variables() -> None:
    m = PGModule(name="pg", storage_gb=200)
    vars = m.get_variables()
    assert vars["storage_gb"] == 200


def test_network_module_hcl() -> None:
    n = NetworkModule(name="vpc", vpc_cidr="10.0.0.0/16")
    hcl = n.to_hcl()
    assert "10.0.0.0/16" in hcl


def test_network_module_resources() -> None:
    n = NetworkModule(name="network")
    resources = n.get_resources()
    assert len(resources) == 1
    assert resources[0].resource_type == "aws_vpc"


def test_generator_resource_count() -> None:
    gen = TerraformGenerator(provider=ResourceProvider.GCP, region="us-central1")
    for i in range(3):
        gen.add_pg_instance(PGInstance(name=f"pg-{i}", instance_class="db.t3.micro", storage_gb=10))
    assert gen.resource_count == 3
