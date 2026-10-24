from __future__ import annotations

from churn_predict.models import Customer
from churn_predict.pipeline import ChurnPipeline


def test_high_risk_customer() -> None:
    pipeline = ChurnPipeline()
    customer = Customer(customer_id="c1", tenure_months=2, monthly_charges=80.0, support_tickets=5)
    score = pipeline.run(customer)
    assert score.risk_level == "high"


def test_low_risk_customer() -> None:
    pipeline = ChurnPipeline()
    customer = Customer(
        customer_id="c2", tenure_months=24, monthly_charges=20.0, total_charges=500.0
    )
    score = pipeline.run(customer)
    assert score.risk_level == "low"


def test_medium_risk_customer() -> None:
    pipeline = ChurnPipeline()
    customer = Customer(customer_id="c3", tenure_months=6, monthly_charges=60.0)
    score = pipeline.run(customer)
    assert score.risk_level in ("medium", "high")


def test_probability_range() -> None:
    pipeline = ChurnPipeline()
    customer = Customer(customer_id="c4")
    score = pipeline.run(customer)
    assert 0.0 <= score.probability <= 1.0


def test_customer_id_preserved() -> None:
    pipeline = ChurnPipeline()
    customer = Customer(customer_id="test-id")
    score = pipeline.run(customer)
    assert score.customer_id == "test-id"
