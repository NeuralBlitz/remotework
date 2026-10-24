from __future__ import annotations

from abc import ABC, abstractmethod

from pg_pooler.models import ConnectionInfo


class PoolBackend(ABC):
    @abstractmethod
    def create_connection(self, conn_id: str) -> ConnectionInfo: ...

    @abstractmethod
    def destroy_connection(self, conn: ConnectionInfo) -> None: ...

    @abstractmethod
    def ping(self, conn: ConnectionInfo) -> bool: ...

    @property
    @abstractmethod
    def backend_name(self) -> str: ...


class PgBouncerBackend(PoolBackend):
    def create_connection(self, conn_id: str) -> ConnectionInfo:
        return ConnectionInfo(conn_id=conn_id, backend=self.backend_name, active=True)

    def destroy_connection(self, conn: ConnectionInfo) -> None:
        conn.active = False

    def ping(self, conn: ConnectionInfo) -> bool:
        return conn.active

    @property
    def backend_name(self) -> str:
        return "pgbouncer"


class PgpoolBackend(PoolBackend):
    def create_connection(self, conn_id: str) -> ConnectionInfo:
        return ConnectionInfo(conn_id=conn_id, backend=self.backend_name, active=True)

    def destroy_connection(self, conn: ConnectionInfo) -> None:
        conn.active = False

    def ping(self, conn: ConnectionInfo) -> bool:
        return conn.active

    @property
    def backend_name(self) -> str:
        return "pgpool"
