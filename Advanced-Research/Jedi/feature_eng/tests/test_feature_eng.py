"""Tests for feature_eng."""
from __future__ import annotations

from src.feature_eng import aggregate_features, create_features
from src.feature_eng.models import Feature, FeatureSet


def test_create_features_empty():
    result = create_features([])
    assert isinstance(result, FeatureSet)
    assert len(result.features) == 0

def test_create_features_single():
    data = [{"name": "f1", "value": 1.0}]
    result = create_features(data)
    assert len(result.features) == 1
    assert result.features[0].name == "f1"

def test_create_features_multiple():
    data = [{"name": "f1", "value": 1.0}, {"name": "f2", "value": 2.0}]
    result = create_features(data)
    assert len(result.features) == 2

def test_aggregate_features_empty():
    fs = FeatureSet(features=[])
    result = aggregate_features(fs)
    assert result["count"] == 0

def test_aggregate_features():
    fs = FeatureSet(features=[])
    fs.features = [
        Feature(name="f1", value=10.0, timestamp=0.0),
        Feature(name="f2", value=20.0, timestamp=0.0),
    ]
    result = aggregate_features(fs)
    assert result["count"] == 2
    assert result["sum"] == 30.0
    assert result["avg"] == 15.0

def test_feature_set_to_dict():
    fs = FeatureSet(features=[])
    assert isinstance(fs.to_dict(), dict)
