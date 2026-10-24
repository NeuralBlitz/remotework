from dataclasses import dataclass, field
from enum import Enum


class ReplicaRegion(Enum):
    US_EAST = "us-east"
    US_WEST = "us-west"
    EU_WEST = "eu-west"
    AP_SOUTH = "ap-south"
    AP_NORTH = "ap-north"


@dataclass
class ReplicaNode:
    name: str
    host: str
    port: int
    region: ReplicaRegion
    latency_ms: float = 0.0
    healthy: bool = True
    load: float = 0.0

    def __str__(self) -> str:
        return f"{self.name} ({self.region.value})"


@dataclass
class RouteDecision:
    node: ReplicaNode
    strategy: str
    latency_ms: float
    score: float

    @property
    def endpoint(self) -> str:
        return f"{self.node.host}:{self.node.port}"
