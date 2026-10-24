from __future__ import annotations

from dataclasses import dataclass, field

from iac_terraform.models import PGInstance, ResourceProvider, TerraformResource


@dataclass
class TerraformConfig:
    provider: ResourceProvider
    region: str
    resources: list[TerraformResource] = field(default_factory=list)
    variables: dict[str, str] = field(default_factory=dict)
    outputs: dict[str, str] = field(default_factory=dict)

    def to_hcl(self) -> str:
        parts: list[str] = []
        parts.append(f'provider "{self.provider.value}" {{')
        parts.append(f'  region = "{self.region}"')
        parts.append("}")
        parts.append("")

        for var_name, var_desc in self.variables.items():
            parts.append(f'variable "{var_name}" {{')
            parts.append(f'  description = "{var_desc}"')
            parts.append("}")
            parts.append("")

        for resource in self.resources:
            parts.append(resource.to_hcl())
            parts.append("")

        for out_name, out_value in self.outputs.items():
            parts.append(f'output "{out_name}" {{')
            parts.append(f"  value = {out_value}")
            parts.append("}")
            parts.append("")

        return "\n".join(parts)


class TerraformGenerator:
    def __init__(self, provider: ResourceProvider, region: str) -> None:
        self.config = TerraformConfig(provider=provider, region=region)

    def add_pg_instance(self, instance: PGInstance) -> None:
        self.config.resources.append(instance.to_resource())

    def add_variable(self, name: str, description: str) -> None:
        self.config.variables[name] = description

    def add_output(self, name: str, value: str) -> None:
        self.config.outputs[name] = value

    def add_resource(self, resource: TerraformResource) -> None:
        self.config.resources.append(resource)

    def generate(self) -> str:
        return self.config.to_hcl()

    @property
    def resource_count(self) -> int:
        return len(self.config.resources)

    @property
    def variable_count(self) -> int:
        return len(self.config.variables)
