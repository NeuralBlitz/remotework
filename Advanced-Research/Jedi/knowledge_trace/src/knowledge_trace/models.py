from dataclasses import dataclass, field


@dataclass
class Node:
    node_id: str
    name: str
    node_type: str
    parents: list[str] = field(default_factory=list)
    properties: dict = field(default_factory=dict)

    @property
    def depth(self) -> int:
        return len(self.parents)


@dataclass
class Lineage:
    root: Node
    nodes: list[Node]

    def find_node(self, node_id: str) -> Node | None:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None

    def get_ancestors(self, node_id: str) -> list[Node]:
        ancestors = []
        node = self.find_node(node_id)
        while node and node.parents:
            for parent_id in node.parents:
                parent = self.find_node(parent_id)
                if parent and parent not in ancestors:
                    ancestors.append(parent)
                node = parent
        return ancestors


def build_lineage(root_id: str, edges: list[tuple[str, str]]) -> Lineage:
    nodes_dict: dict[str, Node] = {}
    for node_id, parent_id in edges:
        if node_id not in nodes_dict:
            nodes_dict[node_id] = Node(node_id, f"Node_{node_id}", "unknown")
        if parent_id not in nodes_dict:
            nodes_dict[parent_id] = Node(parent_id, f"Node_{parent_id}", "unknown")
        nodes_dict[node_id].parents.append(parent_id)

    root = nodes_dict.get(root_id, Node(root_id, "Root", "root"))
    return Lineage(root, list(nodes_dict.values()))


def trace_provenance(node_id: str, edges: list[tuple[str, str]]) -> list[str]:
    ancestors = []
    for child, parent in edges:
        if child == node_id:
            ancestors.append(parent)
    return ancestors


def calculate_impact(node_id: str, edges: list[tuple[str, str]]) -> int:
    impacted = {node_id}
    for child, parent in edges:
        if parent in impacted:
            impacted.add(child)
    return len(impacted)
