from dataclasses import dataclass
from typing import Any


@dataclass
class Config:
    enabled: bool = True
    threshold: float = 0.5
    max_retries: int = 3


@dataclass
class Result:
    success: bool
    data: Any = None
    error: str | None = None
