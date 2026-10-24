"""Query router — intercepts SQL and routes to the correct shard."""

from __future__ import annotations

import logging
import re

from pg_sharding.models import QueryContext, TenantRoute
from pg_sharding.router import ShardMap

logger = logging.getLogger(__name__)

TENANT_PATTERNS = [
    re.compile(r"WHERE\s+.*?tenant_id\s*=\s*'([^']+)'", re.IGNORECASE),
    re.compile(r"WHERE\s+.*?tenant_id\s*=\s*(\d+)", re.IGNORECASE),
    re.compile(r"tenant_id\s*=\s*'([^']+)'", re.IGNORECASE),
]


class QueryRouter:
    """Parses SQL queries and extracts tenant routing information."""

    def __init__(self, shard_map: ShardMap) -> None:
        self.shard_map = shard_map

    def parse(self, sql: str) -> QueryContext:
        """Extract routing context from a SQL query."""
        tenant_id = self._extract_tenant_id(sql)
        table_name = self._extract_table_name(sql)
        is_write = sql.strip().upper().startswith(("INSERT", "UPDATE", "DELETE"))
        return QueryContext(
            original_sql=sql,
            tenant_id=tenant_id,
            table_name=table_name,
            is_write=is_write,
        )

    def _extract_tenant_id(self, sql: str) -> str | None:
        for pattern in TENANT_PATTERNS:
            match = pattern.search(sql)
            if match:
                return match.group(1)
        return None

    def _extract_table_name(self, sql: str) -> str | None:
        match = re.search(r"(?:FROM|INTO|UPDATE)\s+(\w+)", sql, re.IGNORECASE)
        return match.group(1) if match else None


class TenantRoutingProxy:
    """Proxy that intercepts queries and routes them to the correct shard.

    Usage::
        proxy = TenantRoutingProxy(shard_map)
        route = proxy.route_query("SELECT * FROM orders WHERE tenant_id = 'acme'")
        print(route.shard_id, route.host)
    """

    def __init__(self, shard_map: ShardMap) -> None:
        self.shard_map = shard_map
        self.query_router = QueryRouter(shard_map)

    def route_query(self, sql: str, tenant_id: str | None = None) -> TenantRoute:
        """Route a query to the correct shard based on tenant_id."""
        ctx = self.query_router.parse(sql)
        effective_tenant = tenant_id or ctx.tenant_id

        if effective_tenant is None:
            raise ValueError("Cannot route query: no tenant_id found")

        shard_id = self.shard_map.get_shard_for_tenant(effective_tenant)
        shard_info = self.shard_map.get_shard_info(shard_id)

        if shard_info is None:
            raise ValueError(f"Shard {shard_id} not found")

        return TenantRoute(
            tenant_id=effective_tenant,
            shard_id=shard_id,
            host=shard_info.host,
            port=shard_info.port,
            database=shard_info.database,
        )

    def execute(self, sql: str, tenant_id: str | None = None) -> TenantRoute:
        """Route and return connection info for execution."""
        route = self.route_query(sql, tenant_id)
        logger.info(
            "Routed tenant %s to shard %d at %s:%d",
            route.tenant_id,
            route.shard_id,
            route.host,
            route.port,
        )
        return route
