#!/usr/bin/env python3
"""Main entry point for mission_sim."""

from src.mission_sim.models import Config, BaseModel


def main() -> None:
    config = Config(name="mission_sim", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
