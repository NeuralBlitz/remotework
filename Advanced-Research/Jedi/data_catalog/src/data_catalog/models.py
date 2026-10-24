from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DataAsset:
    name: str
    schema: str
    location: str

@dataclass
class CatalogEntry:
    asset: DataAsset
    metadata: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        return {
            "asset": {
                "name": self.asset.name,
                "schema": self.asset.schema,
                "location": self.asset.location,
            },
            "metadata": self.metadata,
        }
