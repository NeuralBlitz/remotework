"""Tests for pg_graph."""

from __future__ import annotations

import pytest

from pg_graph.composite import FriendTree, GraphTree
from pg_graph.models import Edge, Node
from pg_graph.traversal import TraversalEngine


class TestNode:
    def test_create_node(self) -> None:
        node = Node(node_id="1", name="Alice")
        assert node.label == "Alice"
        assert node.degree == 0

    def test_add_edge(self) -> None:
        node = Node(node_id="1", name="Alice")
        edge = Edge(source_id="1", target_id="2")
        node.add_edge(edge)
        assert node.degree == 1
        assert node.neighbors() == ["2"]

    def test_depth_is_zero(self) -> None:
        node = Node(node_id="1", name="Alice")
        assert node.depth() == 0


class TestEdge:
    def test_reversed(self) -> None:
        edge = Edge(source_id="a", target_id="b", weight=2.0)
        rev = edge.reversed()
        assert rev.source_id == "b"
        assert rev.target_id == "a"
        assert rev.weight == 2.0


class TestGraphTree:
    def test_empty_tree_depth(self) -> None:
        tree = GraphTree(root_id="root")
        assert tree.depth() == 0
        assert tree.size == 0

    def test_add_node(self) -> None:
        tree = GraphTree(root_id="root")
        node = Node(node_id="1", name="Alice")
        tree.add_node(node)
        assert tree.size == 1
        assert tree.get_node("1") is node

    def test_collect_edges(self) -> None:
        tree = GraphTree(root_id="root")
        n1 = Node(node_id="1", name="A")
        n2 = Node(node_id="2", name="B")
        n1.add_edge(Edge(source_id="1", target_id="2"))
        tree.add_component(n1)
        tree.add_component(n2)
        assert len(tree.collect_edges()) == 1


class TestFriendTree:
    def test_add_friendship(self) -> None:
        tree = FriendTree(root_id="social")
        tree.add_node(Node(node_id="a", name="Alice"))
        tree.add_node(Node(node_id="b", name="Bob"))
        tree.add_friendship("a", "b")
        assert tree.friend_count("a") == 1
        assert tree.friend_count("b") == 1

    def test_mutual_friends(self) -> None:
        tree = FriendTree(root_id="social")
        for uid in ["a", "b", "c", "d"]:
            tree.add_node(Node(node_id=uid, name=uid))
        tree.add_friendship("a", "c")
        tree.add_friendship("a", "d")
        tree.add_friendship("b", "c")
        tree.add_friendship("b", "d")
        mutual = tree.mutual_friends("a", "b")
        assert mutual == {"c", "d"}


class TestTraversalEngine:
    @pytest.fixture()
    def engine(self) -> TraversalEngine:
        tree = FriendTree(root_id="net")
        for uid in ["a", "b", "c", "d", "e", "f"]:
            tree.add_node(Node(node_id=uid, name=uid))
        tree.add_friendship("a", "b")
        tree.add_friendship("b", "c")
        tree.add_friendship("c", "d")
        tree.add_friendship("a", "e")
        tree.add_friendship("f", "f")
        return TraversalEngine(tree)

    def test_shortest_path_direct(self, engine: TraversalEngine) -> None:
        path = engine.shortest_path("a", "b")
        assert path == ["a", "b"]

    def test_shortest_path_indirect(self, engine: TraversalEngine) -> None:
        path = engine.shortest_path("a", "d")
        assert path == ["a", "b", "c", "d"]

    def test_shortest_path_same_node(self, engine: TraversalEngine) -> None:
        assert engine.shortest_path("a", "a") == ["a"]

    def test_shortest_path_unreachable(self, engine: TraversalEngine) -> None:
        assert engine.shortest_path("a", "f") is None

    def test_degree_of_separation(self, engine: TraversalEngine) -> None:
        assert engine.degree_of_separation("a", "b") == 1
        assert engine.degree_of_separation("a", "d") == 3

    def test_reachable_nodes(self, engine: TraversalEngine) -> None:
        reachable = engine.reachable_nodes("a")
        assert reachable == {"b", "c", "d", "e"}

    def test_connected_components(self, engine: TraversalEngine) -> None:
        components = engine.connected_components()
        assert len(components) == 2

    def test_common_neighbors(self, engine: TraversalEngine) -> None:
        tree = FriendTree(root_id="net")
        for uid in ["a", "b", "c", "d"]:
            tree.add_node(Node(node_id=uid, name=uid))
        tree.add_friendship("a", "c")
        tree.add_friendship("a", "d")
        tree.add_friendship("b", "c")
        tree.add_friendship("b", "d")
        eng = TraversalEngine(tree)
        assert eng.common_neighbors("a", "b") == {"c", "d"}
