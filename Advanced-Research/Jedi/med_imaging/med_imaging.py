#!/usr/bin/env python3
"""Main entry point for med_imaging."""

from src.med_imaging.models import Config, BaseModel


def main() -> None:
    config = Config(name="med_imaging", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
