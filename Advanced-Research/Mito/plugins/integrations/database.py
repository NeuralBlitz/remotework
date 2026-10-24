"""
Database Plugin
Execute queries on PostgreSQL, MySQL, and SQLite.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger("mito.plugins.database")


class DatabaseClient:
    def __init__(self, uri: str = None):
        self.uri = uri or os.environ.get("DATABASE_URL", "")
        self._engine = None
        self._engine_type = None
        self._parse_uri()

    def _parse_uri(self):
        if not self.uri:
            return
        if self.uri.startswith("postgresql") or self.uri.startswith("postgres"):
            self._engine_type = "postgresql"
        elif self.uri.startswith("mysql"):
            self._engine_type = "mysql"
        elif self.uri.startswith("sqlite"):
            self._engine_type = "sqlite"
        else:
            self._engine_type = "unknown"

    def _get_conn(self):
        if self._engine_type == "postgresql":
            try:
                import psycopg2
                return psycopg2.connect(self.uri)
            except ImportError:
                try:
                    import psycopg2
                    conn = psycopg2.connect(
                        host=os.environ.get("PGHOST", "localhost"),
                        port=os.environ.get("PGPORT", "5432"),
                        dbname=os.environ.get("PGDATABASE", "postgres"),
                        user=os.environ.get("PGUSER", "postgres"),
                        password=os.environ.get("PGPASSWORD", ""),
                    )
                    return conn
                except ImportError:
                    raise ImportError("psycopg2 not installed: pip install psycopg2-binary")
        elif self._engine_type == "mysql":
            try:
                import pymysql
                return pymysql.connect(
                    host=os.environ.get("MYSQL_HOST", "localhost"),
                    port=int(os.environ.get("MYSQL_PORT", "3306")),
                    user=os.environ.get("MYSQL_USER", "root"),
                    password=os.environ.get("MYSQL_PASSWORD", ""),
                    database=os.environ.get("MYSQL_DATABASE", ""),
                    charset="utf8mb4",
                )
            except ImportError:
                raise ImportError("pymysql not installed: pip install pymysql")
        elif self._engine_type == "sqlite":
            import sqlite3
            db_path = self.uri.replace("sqlite:///", "").replace("sqlite:///", "")
            if db_path == "":
                db_path = ":memory:"
            return sqlite3.connect(db_path)
        else:
            raise ValueError(f"Unknown database engine: {self._engine_type}")

    def query(self, sql: str, params: tuple = None, limit: int = 1000) -> Dict:
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            if sql.strip().upper().startswith(("SELECT", "SHOW", "DESCRIBE", "EXPLAIN")):
                rows = cursor.fetchmany(limit)
                columns = [d[0] for d in cursor.description] if cursor.description else []
                return {"type": "select", "columns": columns, "rows": rows, "count": len(rows)}
            else:
                conn.commit()
                return {"type": "write", "affected": cursor.rowcount, "lastrowid": cursor.lastrowid}
        finally:
            conn.close()

    def tables(self) -> List[str]:
        if self._engine_type == "postgresql":
            result = self.query("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'")
        elif self._engine_type == "mysql":
            result = self.query("SHOW TABLES")
            return [list(r)[0] for r in result.get("rows", [])]
        elif self._engine_type == "sqlite":
            result = self.query("SELECT name FROM sqlite_master WHERE type='table'")
        else:
            return []
        return [r[0] for r in result.get("rows", [])]

    def schema(self, table: str) -> Dict:
        if self._engine_type == "postgresql":
            return self.query(f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = '{table}'")
        elif self._engine_type == "mysql":
            return self.query(f"DESCRIBE {table}")
        elif self._engine_type == "sqlite":
            return self.query(f"PRAGMA table_info({table})")
        return {"error": f"Schema not supported for {self._engine_type}"}

    def insert(self, table: str, data: Dict) -> Dict:
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        return self.query(sql, tuple(data.values()))

    def execute_file(self, filepath: str) -> List[Dict]:
        path = os.path.expanduser(filepath)
        with open(path) as f:
            sql = f.read()
        results = []
        for stmt in sql.split(";"):
            stmt = stmt.strip()
            if stmt:
                results.append(self.query(stmt))
        return results


def db_query_cmd(sql: str = "") -> Dict:
    """Execute a SQL query and return results."""
    return DatabaseClient().query(sql)


def db_tables_cmd() -> List[str]:
    """List all tables in the database."""
    return DatabaseClient().tables()


def db_schema_cmd(table: str = "") -> Dict:
    """Get the schema (columns) of a table."""
    return DatabaseClient().schema(table)


def db_insert_cmd(table: str = "", data: str = "{}") -> Dict:
    """Insert a row into a table. data is a JSON object."""
    import json
    return DatabaseClient().insert(table, json.loads(data))


def register(plugin):
    plugin.register_command("db_query", db_query_cmd)
    plugin.register_command("db_tables", db_tables_cmd)
    plugin.register_command("db_schema", db_schema_cmd)
    plugin.register_command("db_insert", db_insert_cmd)
    plugin.set_resource("client_class", DatabaseClient)


PLUGIN_METADATA = {
    "name": "database",
    "version": "1.0.0",
    "description": "PostgreSQL, MySQL, SQLite - query, tables, schema, insert",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["database", "sql", "postgresql", "mysql", "sqlite", "query"],
    "dependencies": [],
    "permissions": ["network_access", "read_files"],
    "min_mito_version": "1.0.1",
}


database_plugin = {"metadata": PLUGIN_METADATA, "register": register}
