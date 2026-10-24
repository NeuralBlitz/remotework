#!/usr/bin/env python3
""" water_quality - main entry point """

import argparse
from water_quality.models import create_model, predict


def main() -> None:
    parser = argparse.ArgumentParser(description="Water quality monitoring and analysis")
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
