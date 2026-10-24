from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Feature:
    name: str
    value: float
    timestamp: float

@dataclass
class FeatureSet:
    features: list[Feature] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        features_list = [
            {
                "name": f.name,
                "value": f.value,
                "timestamp": f.timestamp,
            }
            for f in self.features
        ]
        return {"features": features_list}
