#!/usr/bin/env python3
"""Main entry point for protein_bind."""

from src.protein_bind.models import Config, BaseModel


def main() -> None:
    config = Config(name="protein_bind", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
