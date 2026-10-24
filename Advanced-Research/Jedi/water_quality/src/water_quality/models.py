from dataclasses import dataclass
from typing import Any


@dataclass
class BaseModel:
    id: str
    name: str
    version: str = "0.1.0"
    enabled: bool = True


@dataclass
class Prediction:
    model_id: str
    input_data: dict[str, Any]
    output: dict[str, Any] | None = None
    confidence: float = 0.0
    timestamp: str | None = None


def create_model(name: str, version: str = "0.1.0") -> BaseModel:
    return BaseModel(id=name.lower().replace(" ", "_"), name=name, version=version)


def predict(model: BaseModel, data: dict[str, Any]) -> Prediction:
    return Prediction(model_id=model.id, input_data=data, confidence=0.85)
