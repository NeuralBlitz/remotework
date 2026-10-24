"""API gateway routing."""
from __future__ import annotations

from .models import Request, Route

__all__ = ["Route", "Request", "create_route", "match_route"]

def create_route(path: str, method: str, handler: str) -> Route:
    return Route(path=path, method=method, handler=handler)

def match_route(routes: list[Route], request: Request) -> Route | None:
    for route in routes:
        if route.path == request.path and route.method == request.method:
            return route
    return None
