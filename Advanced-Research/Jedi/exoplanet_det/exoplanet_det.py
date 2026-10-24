#!/usr/bin/env python3
"""Main entry point for exoplanet_det."""

from src.exoplanet_det.models import Config, BaseModel


def main() -> None:
    config = Config(name="exoplanet_det", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
