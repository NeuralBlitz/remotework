from __future__ import annotations

from dataclasses import dataclass

from .models import ChurnScore, Customer


@dataclass
class FeatureExtractor:
    def extract(self, customer: Customer) -> dict[str, float]:
        return {
            "tenure_months": float(customer.tenure_months),
            "monthly_charges": customer.monthly_charges,
            "total_charges": customer.total_charges,
            "support_tickets": float(customer.support_tickets),
        }


@dataclass
class ChurnModel:
    threshold: float = 0.5

    def predict(self, features: dict[str, float]) -> float:
        risk = 0.0
        risk += 0.3 if features.get("tenure_months", 12) < 6 else 0.0
        risk += 0.3 if features.get("monthly_charges", 0) > 50 else 0.0
        risk += 0.2 if features.get("support_tickets", 0) > 3 else 0.0
        risk += 0.2 if features.get("total_charges", 0) < 100 else 0.0
        return min(risk, 1.0)


class ChurnPipeline:
    def __init__(self) -> None:
        self.feature_extractor = FeatureExtractor()
        self.model = ChurnModel()

    def run(self, customer: Customer) -> ChurnScore:
        features = self.feature_extractor.extract(customer)
        probability = self.model.predict(features)
        return ChurnScore(
            customer_id=customer.customer_id,
            probability=probability,
            risk_level="high" if probability > 0.6 else "medium" if probability > 0.3 else "low",
        )

