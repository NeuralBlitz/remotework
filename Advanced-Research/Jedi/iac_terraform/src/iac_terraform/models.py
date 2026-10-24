from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ResourceProvider(str, Enum):
    AWS = "aws"
    GCP = "google"
    AZURE = "azurerm"


@dataclass
class TerraformResource:
    resource_type: str
    name: str
    provider: ResourceProvider
    properties: dict[str, Any] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)

    def to_hcl(self) -> str:
        lines = [f'resource "{self.resource_type}" "{self.name}" {{']
        for key, value in self.properties.items():
            if isinstance(value, str):
                lines.append(f'  {key} = "{value}"')
            elif isinstance(value, bool):
                lines.append(f"  {key} = {'true' if value else 'false'}")
            elif isinstance(value, list):
                lines.append(f"  {key} = {value}")
            else:
                lines.append(f"  {key} = {value}")
        lines.append("}")
        return "\n".join(lines)


@dataclass
class PGInstance:
    name: str
    instance_class: str
    storage_gb: int
    engine_version: str = "16.2"
    multi_az: bool = True
    publicly_accessible: bool = False
    backup_retention_days: int = 7
    tags: dict[str, str] = field(default_factory=dict)

    def to_resource(self) -> TerraformResource:
        return TerraformResource(
            resource_type="aws_db_instance",
            name=self.name,
            provider=ResourceProvider.AWS,
            properties={
                "engine": "postgres",
                "engine_version": self.engine_version,
                "instance_class": self.instance_class,
                "allocated_storage": self.storage_gb,
                "multi_az": self.multi_az,
                "publicly_accessible": self.publicly_accessible,
                "backup_retention_period": self.backup_retention_days,
            },
        )
