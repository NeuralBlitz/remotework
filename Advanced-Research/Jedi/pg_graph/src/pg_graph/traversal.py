"""Graph traversal algorithms."""

from __future__ import annotations

from collections import deque

from pg_graph.composite import FriendTree


class TraversalEngine:
    """Engine for graph traversal queries."""

    def __init__(self, graph: FriendTree) -> None:
        self._graph = graph

    def shortest_path(self, source: str, target: str) -> list[str] | None:
        """BFS shortest path between two nodes."""
        if source == target:
            return [source]
        if source not in self._graph.adjacency:
            return None

        visited: set[str] = {source}
        queue: deque[list[str]] = deque([[source]])

        while queue:
            path = queue.popleft()
            current = path[-1]
            for neighbor in self._graph.adjacency.get(current, set()):
                if neighbor == target:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
        return None

    def degree_of_separation(self, source: str, target: str) -> int:
        """Return the number of hops between two users, or -1 if unreachable."""
        path = self.shortest_path(source, target)
        if path is None:
            return -1
        return len(path) - 1

    def reachable_nodes(self, source: str) -> set[str]:
        """Return all nodes reachable from source."""
        if source not in self._graph.adjacency:
            return set()
        visited: set[str] = set()
        queue: deque[str] = deque([source])
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            for neighbor in self._graph.adjacency.get(node, set()):
                if neighbor not in visited:
                    queue.append(neighbor)
        return visited - {source}

    def connected_components(self) -> list[set[str]]:
        """Find all connected components."""
        all_nodes = set(self._graph.adjacency.keys())
        components: list[set[str]] = []
        remaining = set(all_nodes)

        while remaining:
            start = next(iter(remaining))
            component = self.reachable_nodes(start) | {start}
            components.append(component)
            remaining -= component

        return components

    def common_neighbors(self, node_a: str, node_b: str) -> set[str]:
        """Find common neighbors of two nodes."""
        neighbors_a = self._graph.adjacency.get(node_a, set())
        neighbors_b = self._graph.adjacency.get(node_b, set())
        return neighbors_a & neighbors_b
