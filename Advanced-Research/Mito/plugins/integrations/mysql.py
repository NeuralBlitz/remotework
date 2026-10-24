"""MySQL Plugin"""
import os
from typing import Dict, List

class MySQLClient:
    def __init__(self, dsn: str = None):
        self.dsn = dsn or os.environ.get("MYSQL_URL", "mysql://root:password@localhost:3306/mito")
    def query(self, sql: str, params: tuple = None) -> List[Dict]:
        import mysql.connector
        conn = mysql.connector.connect(dsn=self.dsn)
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchall()
    def execute(self, sql: str, params: tuple = None) -> int:
        import mysql.connector
        conn = mysql.connector.connect(dsn=self.dsn)
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.rowcount

def register(plugin): plugin.set_resource("client_class", MySQLClient)
mysql_plugin = {"metadata": {"name": "mysql", "version": "1.0.0", "description": "MySQL database", "author": "Mito Team", "license": "MIT", "tags": ["mysql", "database", "sql"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
