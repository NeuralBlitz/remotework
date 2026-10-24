"""
Mito Knowledge Graph
Simple in-memory knowledge graph with entities, relations, and queries
"""

import json
import logging
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger("mito.knowledge")


@dataclass
class Entity:
    id: str
    type: str
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)
    aliases: List[str] = field(default_factory=list)


@dataclass
class Relation:
    source: str
    target: str
    type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0


class KnowledgeGraph:
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relations: List[Relation] = []
        self._index_type: Dict[str, Set[str]] = {}
        self._index_name: Dict[str, Set[str]] = {}

    def add_entity(self, entity: Entity) -> str:
        self.entities[entity.id] = entity
        self._index_type.setdefault(entity.type, set()).add(entity.id)
        self._index_name.setdefault(entity.name.lower(), set()).add(entity.id)
        for alias in entity.aliases:
            self._index_name.setdefault(alias.lower(), set()).add(entity.id)
        return entity.id

    def add_relation(self, relation: Relation) -> bool:
        if relation.source not in self.entities or relation.target not in self.entities:
            return False
        self.relations.append(relation)
        return True

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        return self.entities.get(entity_id)

    def find_by_name(self, name: str) -> List[Entity]:
        ids = self._index_name.get(name.lower(), set())
        return [self.entities[id] for id in ids if id in self.entities]

    def find_by_type(self, entity_type: str) -> List[Entity]:
        ids = self._index_type.get(entity_type, set())
        return [self.entities[id] for id in ids if id in self.entities]

    def get_relations(self, entity_id: str, direction: str = "both",
                      relation_type: str = None) -> List[Relation]:
        results = []
        for rel in self.relations:
            if relation_type and rel.type != relation_type:
                continue
            if direction in ("out", "both") and rel.source == entity_id:
                results.append(rel)
            if direction in ("in", "both") and rel.target == entity_id:
                results.append(rel)
        return results

    def get_neighbors(self, entity_id: str, depth: int = 1) -> Set[str]:
        visited = set()
        current = {entity_id}
        for _ in range(depth):
            next_level = set()
            for eid in current:
                if eid in visited:
                    continue
                visited.add(eid)
                for rel in self.relations:
                    if rel.source == eid and rel.target not in visited:
                        next_level.add(rel.target)
                    if rel.target == eid and rel.source not in visited:
                        next_level.add(rel.source)
            current = next_level
        return visited - {entity_id}

    def find_path(self, source: str, target: str, max_depth: int = 5) -> List[List[str]]:
        paths = []
        self._dfs(source, target, [source], set(), paths, max_depth)
        return paths

    def _dfs(self, current: str, target: str, path: List[str],
             visited: Set[str], paths: List[List[str]], max_depth: int):
        if len(path) > max_depth:
            return
        if current == target:
            paths.append(path.copy())
            return
        visited.add(current)
        for rel in self.relations:
            next_node = None
            if rel.source == current:
                next_node = rel.target
            elif rel.target == current:
                next_node = rel.source
            if next_node and next_node not in visited:
                path.append(next_node)
                self._dfs(next_node, target, path, visited, paths, max_depth)
                path.pop()
        visited.discard(current)

    def query(self, entity_type: str = None, name: str = None,
              relation_type: str = None, target_type: str = None) -> List[Dict]:
        results = []
        candidates = list(self.entities.values())
        if entity_type:
            candidates = [e for e in candidates if e.type == entity_type]
        if name:
            candidates = [e for e in candidates if name.lower() in e.name.lower()]

        for entity in candidates:
            entry = {"entity": entity, "relations": []}
            for rel in self.get_relations(entity.id, relation_type=relation_type):
                other_id = rel.target if rel.source == entity.id else rel.source
                other = self.entities.get(other_id)
                if target_type and (not other or other.type != target_type):
                    continue
                entry["relations"].append({"relation": rel, "other": other})
            results.append(entry)
        return results

    def merge(self, other: "KnowledgeGraph"):
        for entity in other.entities.values():
            self.add_entity(entity)
        for rel in other.relations:
            self.add_relation(rel)

    def subgraph(self, entity_ids: Set[str]) -> "KnowledgeGraph":
        kg = KnowledgeGraph()
        for eid in entity_ids:
            if eid in self.entities:
                kg.add_entity(self.entities[eid])
        for rel in self.relations:
            if rel.source in entity_ids and rel.target in entity_ids:
                kg.add_relation(rel)
        return kg

    def save(self, filepath: str):
        data = {
            "entities": {eid: {"id": e.id, "type": e.type, "name": e.name,
                               "properties": e.properties, "aliases": e.aliases}
                         for eid, e in self.entities.items()},
            "relations": [{"source": r.source, "target": r.target, "type": r.type,
                           "properties": r.properties, "weight": r.weight}
                          for r in self.relations],
        }
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def load(self, filepath: str):
        with open(filepath) as f:
            data = json.load(f)
        for eid, edata in data["entities"].items():
            self.add_entity(Entity(**edata))
        for rdata in data["relations"]:
            self.add_relation(Relation(**rdata))

    def get_stats(self) -> Dict:
        types = {}
        for e in self.entities.values():
            types[e.type] = types.get(e.type, 0) + 1
        rel_types = {}
        for r in self.relations:
            rel_types[r.type] = rel_types.get(r.type, 0) + 1
        return {
            "entities": len(self.entities),
            "relations": len(self.relations),
            "entity_types": types,
            "relation_types": rel_types,
        }

    def delete_entity(self, entity_id: str) -> bool:
        if entity_id not in self.entities:
            return False
        entity = self.entities[entity_id]
        self._index_type.get(entity.type, set()).discard(entity_id)
        self._index_name.get(entity.name.lower(), set()).discard(entity_id)
        del self.entities[entity_id]
        self.relations = [r for r in self.relations if r.source != entity_id and r.target != entity_id]
        return True
