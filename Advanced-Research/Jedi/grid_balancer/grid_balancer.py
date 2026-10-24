#!/usr/bin/env python3
"""Main entry point for grid_balancer."""

from src.grid_balancer.models import Config, BaseModel


def main() -> None:
    config = Config(name="grid_balancer", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
