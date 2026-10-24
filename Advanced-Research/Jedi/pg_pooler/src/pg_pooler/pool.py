from __future__ import annotations

import queue

from pg_pooler.bridge import PoolBackend
from pg_pooler.models import ConnectionInfo, PoolConfig, PoolStats


class PoolExhaustedError(Exception):
    pass


class ConnectionPool:
    def __init__(self, config: PoolConfig, backend: PoolBackend) -> None:
        self._config = config
        self._backend = backend
        self._idle: queue.Queue[ConnectionInfo] = queue.Queue()
        self._active: set[str] = set()
        self._conn_counter = 0

    def _make_conn_id(self) -> str:
        self._conn_counter += 1
        return f"conn_{self._conn_counter}"

    def acquire(self, timeout: float | None = None) -> ConnectionInfo:
        timeout = timeout if timeout is not None else self._config.timeout
        try:
            conn = self._idle.get_nowait()
            conn.active = True
            self._active.add(conn.conn_id)
            return conn
        except queue.Empty:
            pass

        if self._active and len(self._active) >= self._config.max_size:
            try:
                conn = self._idle.get(timeout=timeout)
                conn.active = True
                self._active.add(conn.conn_id)
                return conn
            except queue.Empty as exc:
                raise PoolExhaustedError("Connection pool exhausted") from exc

        conn_id = self._make_conn_id()
        conn = self._backend.create_connection(conn_id)
        self._active.add(conn.conn_id)
        return conn

    def release(self, conn: ConnectionInfo) -> None:
        if conn.conn_id not in self._active:
            return
        self._active.discard(conn.conn_id)
        conn.active = False
        self._idle.put(conn)

    def stats(self) -> PoolStats:
        idle = self._idle.qsize()
        return PoolStats(
            total=len(self._active) + idle,
            active=len(self._active),
            idle=idle,
        )

    @property
    def backend(self) -> PoolBackend:
        return self._backend

    def switch_backend(self, new_backend: PoolBackend) -> None:
        while True:
            try:
                conn = self._idle.get_nowait()
                self._backend.destroy_connection(conn)
            except queue.Empty:
                break
        self._active.clear()
        self._backend = new_backend
