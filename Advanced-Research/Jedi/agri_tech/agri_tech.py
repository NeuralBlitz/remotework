#!/usr/bin/env python3
"""Main entry point for agri_tech."""

from src.agri_tech.models import Config, BaseModel


def main() -> None:
    config = Config(name="agri_tech", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
