from __future__ import annotations
from .models import ScentProfile


class GNNPredictor:
    """Mock GNN predictor for smell prediction."""

    def predict(self, molecule_id: str) -> ScentProfile:
        # Simulate prediction
        intensity = len(molecule_id) * 0.1
        pleasantness = 0.5 if "flower" in molecule_id else -0.2
        descriptors = ["sweet", "floral"] if "flower" in molecule_id else ["chemical"]
        return ScentProfile(
            molecule_id=molecule_id,
            intensity=intensity,
            pleasantness=pleasantness,
            descriptors=descriptors,
        )


class OlfactoryFacade:
    """Facade for olfactory perception engine."""

    def __init__(self) -> None:
        self._predictor = GNNPredictor()

    def analyze_scent(self, molecule_id: str) -> ScentProfile:
        return self._predictor.predict(molecule_id)

    def batch_analyze(self, molecule_ids: list[str]) -> list[ScentProfile]:
        return [self.analyze_scent(mid) for mid in molecule_ids]
