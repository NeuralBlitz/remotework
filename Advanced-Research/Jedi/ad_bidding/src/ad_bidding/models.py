from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BidRequest:
    request_id: str
    placement: str = ""
    quality_score: float = 1.0
    max_bid: float = 10.0


@dataclass
class BidResponse:
    request_id: str
    amount: float = 0.0
    winner: bool = False


@dataclass
class Auction:
    auction_id: str
    bids: list[BidResponse] = field(default_factory=list)

