from dataclasses import dataclass
from enum import Enum
from typing import Any


class RetrievalMode(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    BATCH = "batch"


@dataclass(frozen=True)
class FeatureDefinition:
    name: str
    entity_key: str
    description: str = ""
    default: Any = None


@dataclass(frozen=True)
class FeatureValue:
    feature_name: str
    entity_id: str
    value: Any
    retrieved_via: RetrievalMode = RetrievalMode.ONLINE
