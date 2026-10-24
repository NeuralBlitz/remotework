from knowledge_trace import Lineage, Node


def main() -> None:
    root = Node("1", "Dataset", "data")
    child = Node("2", "Model", "model", parents=["1"])
    lineage = Lineage(root, [root, child])
    ancestors = lineage.get_ancestors("2")
    print(f"Root: {root.name}")
    print(f"Ancestors of {child.name}: {[a.name for a in ancestors]}")


if __name__ == "__main__":
    main()
