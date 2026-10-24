from dataclasses import dataclass
from typing import Protocol


@dataclass
class Config:
    name: str
    value: float


class BaseModel(Protocol):
    def predict(self, data: dict) -> dict: ...
    def train(self, data: list[dict]) -> None: ...
