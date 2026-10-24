"""Data lineage tracking."""

from __future__ import annotations

from .models import Edge, Node

__all__ = ["Node", "Edge", "create_node", "create_edge", "get_lineage"]


def create_node(node_id: str, node_type: str, name: str) -> Node:
    return Node(id=node_id, type=node_type, name=name)


def create_edge(source: str, target: str) -> Edge:
    return Edge(source=source, target=target)


def get_lineage(edges: list[Edge]) -> dict[str, list[str] | list[dict[str, str]]]:
    nodes = list(set([e.source for e in edges] + [e.target for e in edges]))
    return {"nodes": nodes, "edges": [e.to_dict() for e in edges]}
