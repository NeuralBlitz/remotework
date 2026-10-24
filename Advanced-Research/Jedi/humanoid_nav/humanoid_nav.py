#!/usr/bin/env python3
"""Main entry point for humanoid_nav."""

from src.humanoid_nav.models import Config, BaseModel


def main() -> None:
    config = Config(name="humanoid_nav", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
