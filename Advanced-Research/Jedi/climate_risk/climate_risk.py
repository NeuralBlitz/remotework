#!/usr/bin/env python3
"""Main entry point for climate_risk."""

from src.climate_risk.models import Config, BaseModel


def main() -> None:
    config = Config(name="climate_risk", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
