from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Customer:
    customer_id: str
    tenure_months: int = 12
    monthly_charges: float = 0.0
    total_charges: float = 0.0
    support_tickets: int = 0


@dataclass
class ChurnScore:
    customer_id: str
    probability: float = 0.0
    risk_level: str = "low"

