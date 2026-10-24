#!/usr/bin/env python3
"""Main entry point for neural_comp."""

from src.neural_comp.models import Config, BaseModel


def main() -> None:
    config = Config(name="neural_comp", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
