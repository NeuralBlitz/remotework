#!/usr/bin/env python3
"""Main entry point for warehouse_bot."""

from src.warehouse_bot.models import Config, BaseModel


def main() -> None:
    config = Config(name="warehouse_bot", value=1.0)
    print(f"Running {config.name} v0.1.0")


if __name__ == "__main__":
    main()
