from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Route:
    path: str
    method: str
    handler: str

@dataclass
class Request:
    path: str
    method: str
    headers: dict[str, str]
