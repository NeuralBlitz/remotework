#!/usr/bin/env python3
"""Main entry point for chip_layout."""

from src.chip_layout.models import Config, BaseModel


def main() -> None:
    config = Config(name="chip_layout", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
