#!/usr/bin/env python3
import sys
from src.oracle_engine import initialize, process, shutdown


def main() -> int:
    if not initialize():
        return 1
    result = process({"input": "data"})
    shutdown()
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
