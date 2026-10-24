#!/usr/bin/env python3
""" env_monitor - main entry point """

import argparse
from env_monitor.models import create_model, predict


def main() -> None:
    parser = argparse.ArgumentParser(description="Environmental monitoring and alerting system")
    parser.add_argument("--name", default="default", help="Model name")
    parser.add_argument("--version", default="0.1.0", help="Model version")
    parser.add_argument("--input", default="{}", help="Input data as JSON")
    args = parser.parse_args()

    model = create_model(args.name, args.version)
    result = predict(model, {"data": args.input})
    print(f"Model: {model.name} v{model.version}")
    print(f"Prediction confidence: {result.confidence}")


if __name__ == "__main__":
    main()
