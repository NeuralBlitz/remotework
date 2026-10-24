#!/usr/bin/env python3
"""Main entry point for smart_building."""

from src.smart_building.models import Config, BaseModel


def main() -> None:
    config = Config(name="smart_building", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
