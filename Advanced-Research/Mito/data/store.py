"""
Mito Data Store
SQLite, in-memory cache, disk cache with TTL, migrations, search
"""

import os
import json
import time
import hashlib
import sqlite3
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from collections import OrderedDict


@dataclass
class Record:
    id: Optional[int]
    data: Dict[str, Any]
    created_at: str
    updated_at: str = ""
    version: int = 1


class SQLiteStore:
    """Full-featured SQLite storage with migrations, search, and transactions."""

    def __init__(self, db_path: str = "mito.db", auto_migrate: bool = True):
        self.db_path = db_path
        self.conn = None
        self._lock = threading.Lock()
        self._init_db()
        if auto_migrate:
            self._migrate()

    def _init_db(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")

    def _migrate(self):
        with self._lock:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    version INTEGER DEFAULT 1
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS embeddings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    embedding BLOB NOT NULL,
                    metadata TEXT DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS kv_store (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    expires_at REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()

    def insert(self, data: Dict) -> int:
        with self._lock:
            cursor = self.conn.execute(
                "INSERT INTO records (data, updated_at) VALUES (?, CURRENT_TIMESTAMP)",
                (json.dumps(data),)
            )
            self.conn.commit()
            return cursor.lastrowid

    def get(self, id: int) -> Optional[Record]:
        cursor = self.conn.execute(
            "SELECT id, data, created_at, updated_at, version FROM records WHERE id = ?", (id,)
        )
        row = cursor.fetchone()
        if row:
            return Record(id=row[0], data=json.loads(row[1]), created_at=row[2],
                         updated_at=row[3], version=row[4])
        return None

    def update(self, id: int, data: Dict) -> bool:
        with self._lock:
            current = self.get(id)
            if not current:
                return False
            cursor = self.conn.execute(
                "UPDATE records SET data = ?, updated_at = CURRENT_TIMESTAMP, version = version + 1 WHERE id = ?",
                (json.dumps(data), id)
            )
            self.conn.commit()
            return cursor.rowcount > 0

    def upsert(self, data: Dict, match_field: str = None, match_value: Any = None) -> int:
        if match_field and match_value is not None:
            existing = self.find_one({match_field: match_value})
            if existing:
                self.update(existing.id, data)
                return existing.id
        return self.insert(data)

    def delete(self, id: int) -> bool:
        with self._lock:
            cursor = self.conn.execute("DELETE FROM records WHERE id = ?", (id,))
            self.conn.commit()
            return cursor.rowcount > 0

    def list(self, limit: int = 100, offset: int = 0) -> List[Record]:
        cursor = self.conn.execute(
            "SELECT id, data, created_at, updated_at, version FROM records ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )
        return [Record(id=r[0], data=json.loads(r[1]), created_at=r[2], updated_at=r[3], version=r[4])
                for r in cursor.fetchall()]

    def find(self, query: Dict, limit: int = 100) -> List[Record]:
        records = self.list(limit=1000)
        results = []
        for record in records:
            match = True
            for key, value in query.items():
                if key not in record.data or record.data[key] != value:
                    match = False
                    break
            if match:
                results.append(record)
            if len(results) >= limit:
                break
        return results

    def find_one(self, query: Dict) -> Optional[Record]:
        results = self.find(query, limit=1)
        return results[0] if results else None

    def search(self, field: str, query: str, limit: int = 50) -> List[Record]:
        cursor = self.conn.execute(
            "SELECT id, data, created_at, updated_at, version FROM records WHERE data LIKE ? LIMIT ?",
            (f"%{query}%", limit)
        )
        return [Record(id=r[0], data=json.loads(r[1]), created_at=r[2], updated_at=r[3], version=r[4])
                for r in cursor.fetchall()]

    def count(self) -> int:
        cursor = self.conn.execute("SELECT COUNT(*) FROM records")
        return cursor.fetchone()[0]

    def exists(self, id: int) -> bool:
        cursor = self.conn.execute("SELECT 1 FROM records WHERE id = ?", (id,))
        return cursor.fetchone() is not None

    def truncate(self):
        with self._lock:
            self.conn.execute("DELETE FROM records")
            self.conn.commit()

    def begin_transaction(self):
        self.conn.execute("BEGIN TRANSACTION")

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def execute_raw(self, sql: str, params: tuple = None) -> List[Dict]:
        cursor = self.conn.execute(sql, params or ())
        cols = [d[0] for d in cursor.description] if cursor.description else []
        return [dict(zip(cols, row)) for row in cursor.fetchall()]

    def kv_get(self, key: str) -> Optional[Any]:
        cursor = self.conn.execute(
            "SELECT value, expires_at FROM kv_store WHERE key = ?", (key,)
        )
        row = cursor.fetchone()
        if row:
            if row[1] > 0 and row[1] < time.time():
                self.kv_delete(key)
                return None
            try:
                return json.loads(row[0])
            except json.JSONDecodeError:
                return row[0]
        return None

    def kv_set(self, key: str, value: Any, ttl: int = 0):
        expires = time.time() + ttl if ttl > 0 else 0
        val = json.dumps(value) if not isinstance(value, str) else value
        with self._lock:
            self.conn.execute(
                "INSERT OR REPLACE INTO kv_store (key, value, expires_at) VALUES (?, ?, ?)",
                (key, val, expires)
            )
            self.conn.commit()

    def kv_delete(self, key: str) -> bool:
        with self._lock:
            cursor = self.conn.execute("DELETE FROM kv_store WHERE key = ?", (key,))
            self.conn.commit()
            return cursor.rowcount > 0

    def kv_keys(self, pattern: str = "%") -> List[str]:
        cursor = self.conn.execute("SELECT key FROM kv_store WHERE key LIKE ?", (pattern,))
        return [row[0] for row in cursor.fetchall()]

    def close(self):
        if self.conn:
            self.conn.close()


class InMemoryCache:
    """LRU cache with TTL support."""

    def __init__(self, max_size: int = 1000):
        self.cache: OrderedDict[str, Dict] = OrderedDict()
        self.max_size = max_size
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            self._misses += 1
            return None
        entry = self.cache[key]
        if entry.get("expires", 0) > 0 and time.time() > entry["expires"]:
            del self.cache[key]
            self._misses += 1
            return None
        self.cache.move_to_end(key)
        self._hits += 1
        return entry["value"]

    def set(self, key: str, value: Any, ttl: int = 0):
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
        expires = time.time() + ttl if ttl > 0 else 0
        self.cache[key] = {"value": value, "expires": expires, "created": time.time()}
        self.cache.move_to_end(key)

    def delete(self, key: str) -> bool:
        if key in self.cache:
            del self.cache[key]
            return True
        return False

    def clear(self):
        self.cache.clear()

    def has(self, key: str) -> bool:
        if key not in self.cache:
            return False
        entry = self.cache[key]
        if entry.get("expires", 0) > 0 and time.time() > entry["expires"]:
            del self.cache[key]
            return False
        return True

    def keys(self) -> List[str]:
        now = time.time()
        return [k for k, v in self.cache.items() if v.get("expires", 0) == 0 or v["expires"] > now]

    def cleanup_expired(self) -> int:
        now = time.time()
        expired = [k for k, v in self.cache.items() if v.get("expires", 0) > 0 and v["expires"] < now]
        for k in expired:
            del self.cache[k]
        return len(expired)

    def get_stats(self) -> Dict:
        total = self._hits + self._misses
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": self._hits / total if total > 0 else 0,
        }


class DiskCache:
    """File-based cache with TTL."""

    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, key: str) -> Path:
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{safe_key}.json"

    def get(self, key: str) -> Optional[Any]:
        path = self._get_path(key)
        if path.exists():
            try:
                with open(path, 'r') as f:
                    entry = json.load(f)
                if entry.get("expires", 0) > 0 and time.time() > entry["expires"]:
                    path.unlink()
                    return None
                return entry.get("value")
            except Exception:
                return None
        return None

    def set(self, key: str, value: Any, ttl: int = 0):
        path = self._get_path(key)
        expires = time.time() + ttl if ttl > 0 else 0
        with open(path, 'w') as f:
            json.dump({"value": value, "expires": expires, "key": key}, f)

    def delete(self, key: str) -> bool:
        path = self._get_path(key)
        if path.exists():
            path.unlink()
            return True
        return False

    def clear(self):
        for f in self.cache_dir.glob("*.json"):
            f.unlink()

    def has(self, key: str) -> bool:
        return self.get(key) is not None

    def cleanup_expired(self) -> int:
        count = 0
        for f in self.cache_dir.glob("*.json"):
            try:
                with open(f) as fh:
                    entry = json.load(fh)
                if entry.get("expires", 0) > 0 and time.time() > entry["expires"]:
                    f.unlink()
                    count += 1
            except Exception:
                pass
        return count


if __name__ == '__main__':
    db = SQLiteStore("test.db")
    db.insert({"type": "test", "value": 123})
    records = db.list()
    print(f"Records: {len(records)}")
    db.close()
