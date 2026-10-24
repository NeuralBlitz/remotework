#!/usr/bin/env python3
"""Main entry point for constellation."""

from src.constellation.models import Config, BaseModel


def main() -> None:
    config = Config(name="constellation", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
