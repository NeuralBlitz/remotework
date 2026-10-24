from __future__ import annotations

from .models import CloudAdapter, CloudProvider, ConnectionInfo, QueryResult


class AWSRDSAdapter(CloudAdapter):
    def __init__(self) -> None:
        self._connected = False
        self._info: ConnectionInfo | None = None

    @property
    def provider(self) -> CloudProvider:
        return CloudProvider.AWS

    def connect(self, info: ConnectionInfo) -> bool:
        self._info = info
        self._connected = True
        return True

    def query(self, sql: str) -> QueryResult:
        if not self._connected:
            msg = "Not connected"
            raise RuntimeError(msg)
        return QueryResult(rows=[], row_count=0, duration_ms=2.5, provider=CloudProvider.AWS)

    def disconnect(self) -> bool:
        self._connected = False
        return True


class AzurePGAdapter(CloudAdapter):
    def __init__(self) -> None:
        self._connected = False
        self._info: ConnectionInfo | None = None

    @property
    def provider(self) -> CloudProvider:
        return CloudProvider.AZURE

    def connect(self, info: ConnectionInfo) -> bool:
        self._info = info
        self._connected = True
        return True

    def query(self, sql: str) -> QueryResult:
        if not self._connected:
            msg = "Not connected"
            raise RuntimeError(msg)
        return QueryResult(rows=[], row_count=0, duration_ms=3.1, provider=CloudProvider.AZURE)

    def disconnect(self) -> bool:
        self._connected = False
        return True


class GCPAdapter(CloudAdapter):
    def __init__(self) -> None:
        self._connected = False
        self._info: ConnectionInfo | None = None

    @property
    def provider(self) -> CloudProvider:
        return CloudProvider.GCP

    def connect(self, info: ConnectionInfo) -> bool:
        self._info = info
        self._connected = True
        return True

    def query(self, sql: str) -> QueryResult:
        if not self._connected:
            msg = "Not connected"
            raise RuntimeError(msg)
        return QueryResult(rows=[], row_count=0, duration_ms=1.8, provider=CloudProvider.GCP)

    def disconnect(self) -> bool:
        self._connected = False
        return True
