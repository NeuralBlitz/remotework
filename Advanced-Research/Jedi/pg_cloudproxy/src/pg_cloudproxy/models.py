from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class CloudProvider(Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


@dataclass
class ConnectionInfo:
    host: str
    port: int
    database: str
    username: str
    provider: CloudProvider
    ssl_mode: str = "require"
    pool_size: int = 10


@dataclass
class QueryResult:
    rows: list[dict[str, object]]
    row_count: int
    duration_ms: float
    provider: CloudProvider


class CloudAdapter(ABC):
    @property
    @abstractmethod
    def provider(self) -> CloudProvider: ...

    @abstractmethod
    def connect(self, info: ConnectionInfo) -> bool: ...

    @abstractmethod
    def query(self, sql: str) -> QueryResult: ...

    @abstractmethod
    def disconnect(self) -> bool: ...
