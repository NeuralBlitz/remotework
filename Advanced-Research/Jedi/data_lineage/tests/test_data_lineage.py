"""Tests for data_lineage."""
from __future__ import annotations

from src.data_lineage import create_edge, create_node, get_lineage


def test_create_node():
    node = create_node("n1", "table", "my_table")
    assert node.id == "n1"
    assert node.type == "table"
    assert node.name == "my_table"

def test_create_edge():
    edge = create_edge("source", "target")
    assert edge.source == "source"
    assert edge.target == "target"

def test_get_lineage_empty():
    result = get_lineage([])
    assert result["nodes"] == []
    assert result["edges"] == []

def test_get_lineage_with_edges():
    edges = [create_edge("a", "b"), create_edge("b", "c")]
    result = get_lineage(edges)
    assert len(result["nodes"]) == 3
    assert len(result["edges"]) == 2

def test_edge_to_dict():
    edge = create_edge("x", "y")
    d = edge.to_dict()
    assert d["source"] == "x"
    assert d["target"] == "y"

def test_lineage_no_duplicates():
    edges = [create_edge("a", "b"), create_edge("a", "b")]
    result = get_lineage(edges)
    assert len(result["nodes"]) == 2
