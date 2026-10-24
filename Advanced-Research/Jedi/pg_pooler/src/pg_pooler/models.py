from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PoolConfig:
    min_size: int = 1
    max_size: int = 10
    timeout: float = 30.0
    dsn: str = "localhost:5432"

    def __post_init__(self) -> None:
        if self.min_size < 0:
            raise ValueError("min_size must be >= 0")
        if self.max_size < 1:
            raise ValueError("max_size must be >= 1")
        if self.min_size > self.max_size:
            raise ValueError("min_size must be <= max_size")


@dataclass
class ConnectionInfo:
    conn_id: str
    backend: str
    active: bool = False


@dataclass
class PoolStats:
    total: int = 0
    active: int = 0
    idle: int = 0
    waiters: int = 0

    @property
    def utilization(self) -> float:
        if self.total == 0:
            return 0.0
        return self.active / self.total
