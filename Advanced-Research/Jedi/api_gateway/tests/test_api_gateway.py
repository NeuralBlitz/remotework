"""Tests for api_gateway."""
from __future__ import annotations

from src.api_gateway import create_route, match_route
from src.api_gateway.models import Request


def test_create_route():
    route = create_route("/users", "GET", "get_users")
    assert route.path == "/users"
    assert route.method == "GET"

def test_match_route_found():
    routes = [create_route("/users", "GET", "get_users")]
    request = Request(path="/users", method="GET", headers={})
    result = match_route(routes, request)
    assert result is not None
    assert result.handler == "get_users"

def test_match_route_not_found():
    routes = [create_route("/users", "GET", "get_users")]
    request = Request(path="/orders", method="GET", headers={})
    result = match_route(routes, request)
    assert result is None

def test_match_route_wrong_method():
    routes = [create_route("/users", "GET", "get_users")]
    request = Request(path="/users", method="POST", headers={})
    result = match_route(routes, request)
    assert result is None

def test_match_route_empty_routes():
    request = Request(path="/users", method="GET", headers={})
    result = match_route([], request)
    assert result is None

def test_match_route_multiple_routes():
    routes = [
        create_route("/users", "GET", "get_users"),
        create_route("/users", "POST", "create_user"),
        create_route("/orders", "GET", "get_orders"),
    ]
    request = Request(path="/users", method="POST", headers={})
    result = match_route(routes, request)
    assert result.handler == "create_user"
