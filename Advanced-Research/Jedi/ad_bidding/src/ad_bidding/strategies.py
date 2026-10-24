from __future__ import annotations

from abc import ABC, abstractmethod

from .models import Auction, BidRequest, BidResponse


class BidStrategy(ABC):
    @abstractmethod
    def bid(self, request: BidRequest) -> BidResponse:
        raise NotImplementedError


class FixedBidStrategy(BidStrategy):
    def __init__(self, amount: float = 1.0) -> None:
        self.amount = amount

    def bid(self, request: BidRequest) -> BidResponse:
        return BidResponse(request_id=request.request_id, amount=self.amount)


class DynamicBidStrategy(BidStrategy):
    def __init__(self, base: float = 0.5, multiplier: float = 1.5) -> None:
        self.base = base
        self.multiplier = multiplier

    def bid(self, request: BidRequest) -> BidResponse:
        amount = self.base * self.multiplier * request.quality_score
        return BidResponse(request_id=request.request_id, amount=amount)


class BudgetAwareBidStrategy(BidStrategy):
    def __init__(self, budget: float = 100.0) -> None:
        self.budget = budget
        self.spent = 0.0

    def bid(self, request: BidRequest) -> BidResponse:
        remaining = self.budget - self.spent
        amount = min(remaining * 0.1, request.max_bid)
        self.spent += amount
        return BidResponse(request_id=request.request_id, amount=amount)


class AuctionEngine:
    def run_auction(self, auction: Auction) -> BidResponse | None:
        if not auction.bids:
            return None
        return max(auction.bids, key=lambda b: b.amount)

