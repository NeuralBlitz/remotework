#!/usr/bin/env python3
"""Main entry point for swarm_coord."""

from src.swarm_coord.models import Config, BaseModel


def main() -> None:
    config = Config(name="swarm_coord", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
