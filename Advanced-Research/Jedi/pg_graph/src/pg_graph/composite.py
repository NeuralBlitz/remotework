"""Composite graph structures."""

from __future__ import annotations

from dataclasses import dataclass, field

from pg_graph.models import Edge, GraphComponent, Node


@dataclass
class GraphTree(GraphComponent):
    """Composite tree of graph nodes."""

    root_id: str
    nodes: dict[str, Node] = field(default_factory=dict)
    _children: list[GraphComponent] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"tree:{self.root_id}"

    def depth(self) -> int:
        if not self._children:
            return 0
        return 1 + max(child.depth() for child in self._children)

    def collect_edges(self) -> list[Edge]:
        edges: list[Edge] = []
        for child in self._children:
            edges.extend(child.collect_edges())
        return edges

    def add_component(self, component: GraphComponent) -> None:
        self._children.append(component)

    def add_node(self, node: Node) -> None:
        self.nodes[node.node_id] = node

    @property
    def size(self) -> int:
        return len(self.nodes)

    def get_node(self, node_id: str) -> Node | None:
        return self.nodes.get(node_id)


@dataclass
class FriendTree(GraphTree):
    """Social network friendship tree with adjacency tracking."""

    adjacency: dict[str, set[str]] = field(default_factory=dict)

    def add_friendship(self, user_a: str, user_b: str, weight: float = 1.0) -> None:
        if user_a not in self.adjacency:
            self.adjacency[user_a] = set()
        if user_b not in self.adjacency:
            self.adjacency[user_b] = set()
        self.adjacency[user_a].add(user_b)
        self.adjacency[user_b].add(user_a)
        edge = Edge(source_id=user_a, target_id=user_b, weight=weight)
        if user_a in self.nodes:
            self.nodes[user_a].add_edge(edge)
        if user_b in self.nodes:
            self.nodes[user_b].add_edge(edge.reversed())

    def mutual_friends(self, user_a: str, user_b: str) -> set[str]:
        friends_a = self.adjacency.get(user_a, set())
        friends_b = self.adjacency.get(user_b, set())
        return friends_a & friends_b

    def friend_count(self, user_id: str) -> int:
        return len(self.adjacency.get(user_id, set()))
