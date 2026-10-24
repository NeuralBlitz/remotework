"""Feature engineering utilities."""

from __future__ import annotations

from .models import Feature, FeatureSet

__all__ = ["Feature", "FeatureSet", "create_features", "aggregate_features"]


def create_features(data: list[dict[str, str | float]]) -> FeatureSet:
    features = [
        Feature(
            name=str(d["name"]),
            value=float(d["value"]),
            timestamp=float(d.get("timestamp", 0.0)),
        )
        for d in data
    ]
    return FeatureSet(features=features)


def aggregate_features(feature_set: FeatureSet) -> dict[str, float]:
    if not feature_set.features:
        return {"count": 0, "sum": 0.0, "avg": 0.0}
    values = [f.value for f in feature_set.features]
    return {
        "count": len(values),
        "sum": sum(values),
        "avg": sum(values) / len(values),
    }
