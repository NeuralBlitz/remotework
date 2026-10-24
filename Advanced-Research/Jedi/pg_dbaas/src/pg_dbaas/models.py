from dataclasses import dataclass
from enum import Enum


class DatabaseTier(Enum):
    DEV = "dev"
    STAGE = "stage"
    PROD = "prod"


@dataclass(frozen=True)
class DatabaseProfile:
    name: str
    tier: DatabaseTier
    host: str
    port: int
    max_connections: int
    storage_gb: int
    backup_enabled: bool
    ssl_required: bool
    cpu_cores: float
    ram_gb: float
    description: str = ""
