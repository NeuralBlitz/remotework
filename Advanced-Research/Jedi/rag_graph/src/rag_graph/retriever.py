from __future__ import annotations

from rag_graph.bridge import GraphBackend
from rag_graph.models import Subgraph, Triplet


class TripletRetriever:
    def __init__(self, backend: GraphBackend) -> None:
        self.backend = backend

    def retrieve_by_head(self, entity: str) -> list[Triplet]:
        return self.backend.get_by_head(entity)

    def retrieve_by_relation(self, relation: str) -> list[Triplet]:
        return self.backend.get_by_relation(relation)


class SubgraphRetriever:
    def __init__(self, backend: GraphBackend) -> None:
        self.backend = backend

    def retrieve_ego(self, center: str, hops: int = 1) -> Subgraph:
        sg = Subgraph()
        visited: set[str] = set()
        frontier = [center]
        for _ in range(hops):
            next_frontier: list[str] = []
            for entity in frontier:
                if entity in visited:
                    continue
                visited.add(entity)
                for t in self.backend.get_neighbors(entity):
                    sg.add_triplet(t)
                    for e in (t.head, t.tail):
                        if e not in visited:
                            next_frontier.append(e)
            frontier = next_frontier
        return sg
