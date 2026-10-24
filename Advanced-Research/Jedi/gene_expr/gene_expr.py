#!/usr/bin/env python3
"""Main entry point for gene_expr."""

from src.gene_expr.models import Config, BaseModel


def main() -> None:
    config = Config(name="gene_expr", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
