#!/usr/bin/env python3
"""Main entry point for sat_routing."""

from src.sat_routing.models import Config, BaseModel


def main() -> None:
    config = Config(name="sat_routing", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
