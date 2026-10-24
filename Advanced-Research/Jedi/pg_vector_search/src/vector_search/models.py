"""Core data models for vector search."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any


class IndexType(str, enum.Enum):
    """Available vector index types."""

    HNSW = "hnsw"
    IVFFLAT = "ivfflat"


class DistanceMetric(str, enum.Enum):
    """Distance metrics for vector similarity."""

    COSINE = "cosine"
    L2 = "l2"
    INNER_PRODUCT = "inner_product"


@dataclass
class IndexConfig:
    """Configuration for a vector index."""

    table_name: str
    column_name: str = "embedding"
    dimensions: int = 1536
    distance_metric: DistanceMetric = DistanceMetric.COSINE
    index_type: IndexType = IndexType.HNSW
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class HNSWConfig:
    """HNSW-specific parameters."""

    m: int = 16
    ef_construction: int = 200
    ef_search: int = 40


@dataclass
class IVFFlatConfig:
    """IVFFlat-specific parameters."""

    lists: int = 100
    probes: int = 10


@dataclass
class SearchResult:
    """A single vector search result."""

    id: str
    score: float
    embedding: list[float] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchQuery:
    """A vector similarity search query."""

    embedding: list[float]
    top_k: int = 10
    filter_expr: str | None = None
    include_embeddings: bool = False
