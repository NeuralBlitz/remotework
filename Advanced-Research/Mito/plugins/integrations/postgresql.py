"""PostgreSQL Plugin"""
import os
from typing import Dict, List, Any

class PostgreSQLClient:
    def __init__(self, dsn: str = None):
        self.dsn = dsn or os.environ.get("DATABASE_URL", "postgresql://localhost:5432/mito")
    def _conn(self):
        import psycopg2
        return psycopg2.connect(self.dsn)
    def query(self, sql: str, params: tuple = None) -> List[Dict]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(sql, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    def execute(self, sql: str, params: tuple = None) -> int:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.rowcount
    def tables(self) -> List[str]:
        return [r["tablename"] for r in self.query("SELECT tablename FROM pg_tables WHERE schemaname='public'")]
    def table_info(self, table: str) -> List[Dict]:
        return self.query("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = %s", (table,))

def register(plugin): plugin.set_resource("client_class", PostgreSQLClient)
postgresql_plugin = {"metadata": {"name": "postgresql", "version": "1.0.0", "description": "PostgreSQL database", "author": "Mito Team", "license": "MIT", "tags": ["postgresql", "database", "sql"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
