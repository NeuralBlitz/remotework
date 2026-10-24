from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from iac_terraform.models import ResourceProvider, TerraformResource


@dataclass
class PGModule:
    name: str
    source: str = "./modules/pg"
    instance_class: str = "db.t3.medium"
    storage_gb: int = 100
    engine_version: str = "16.2"
    subnet_group: str = ""
    security_groups: list[str] = field(default_factory=list)

    def to_hcl(self) -> str:
        lines = [f'module "{self.name}" {{']
        lines.append(f'  source = "{self.source}"')
        lines.append(f'  instance_class = "{self.instance_class}"')
        lines.append(f"  storage_gb = {self.storage_gb}")
        lines.append(f'  engine_version = "{self.engine_version}"')
        if self.subnet_group:
            lines.append(f'  subnet_group = "{self.subnet_group}"')
        if self.security_groups:
            lines.append(f"  security_groups = {self.security_groups}")
        lines.append("}")
        return "\n".join(lines)

    def get_variables(self) -> dict[str, Any]:
        return {
            "instance_class": self.instance_class,
            "storage_gb": self.storage_gb,
            "engine_version": self.engine_version,
        }


@dataclass
class NetworkModule:
    name: str
    vpc_cidr: str = "10.0.0.0/16"
    subnet_cidrs: list[str] = field(default_factory=lambda: ["10.0.1.0/24", "10.0.2.0/24"])
    availability_zones: list[str] = field(default_factory=lambda: ["us-east-1a", "us-east-1b"])
    enable_nat_gateway: bool = True

    def to_hcl(self) -> str:
        lines = [f'module "{self.name}" {{']
        lines.append('  source = "./modules/network"')
        lines.append(f'  vpc_cidr = "{self.vpc_cidr}"')
        lines.append(f"  subnet_cidrs = {self.subnet_cidrs}")
        lines.append(f"  availability_zones = {self.availability_zones}")
        lines.append(f"  enable_nat_gateway = {'true' if self.enable_nat_gateway else 'false'}")
        lines.append("}")
        return "\n".join(lines)

    def get_resources(self) -> list[TerraformResource]:
        return [
            TerraformResource(
                resource_type="aws_vpc",
                name=f"{self.name}_vpc",
                provider=ResourceProvider.AWS,
                properties={"cidr_block": self.vpc_cidr},
            )
        ]
