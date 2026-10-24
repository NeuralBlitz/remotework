from __future__ import annotations

from .models import IsolationLevel, SchemaDefinition, TenantConfig


class SchemaFactory:
    def __init__(self) -> None:
        self._templates: dict[IsolationLevel, list[str]] = {
            IsolationLevel.SCHEMA: ["users", "orders", "settings"],
            IsolationLevel.DATABASE: ["users", "orders", "settings", "audit_log"],
            IsolationLevel.ROW_LEVEL: ["shared_users", "shared_orders"],
        }
        self._created_count = 0

    @property
    def created_count(self) -> int:
        return self._created_count

    def register_template(self, level: IsolationLevel, tables: list[str]) -> None:
        self._templates[level] = tables

    def get_template(self, level: IsolationLevel) -> list[str]:
        return list(self._templates.get(level, []))

    def create_schema(self, config: TenantConfig) -> SchemaDefinition:
        schema_name = f"tenant_{config.tenant_id}"
        tables = self.get_template(config.isolation)
        if len(tables) > config.max_tables:
            msg = f"Template exceeds max tables ({config.max_tables})"
            raise ValueError(msg)

        schema = SchemaDefinition(
            schema_name=schema_name,
            tenant_id=config.tenant_id,
            tables=list(tables),
            owner=config.name,
        )
        self._created_count += 1
        return schema

    def create_custom_schema(
        self, tenant_id: str, name: str, tables: list[str]
    ) -> SchemaDefinition:
        schema = SchemaDefinition(
            schema_name=f"tenant_{tenant_id}",
            tenant_id=tenant_id,
            tables=list(tables),
            owner=name,
        )
        self._created_count += 1
        return schema
