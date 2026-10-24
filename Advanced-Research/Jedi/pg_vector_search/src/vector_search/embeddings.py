"""Embedding loading and batch ingestion."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

from vector_search.strategies import IndexStrategy

logger = logging.getLogger(__name__)


@dataclass
class EmbeddingRecord:
    """A single embedding with its ID and optional metadata."""

    id: str
    embedding: list[float]
    metadata: dict[str, Any] | None = None


class EmbeddingLoader:
    """Handles loading and batching embeddings for ingestion.

    Supports:
    - Batch insertion with configurable batch size
    - Deduplication via UPSERT
    - Dimension validation
    """

    def __init__(self, strategy: IndexStrategy, batch_size: int = 1000) -> None:
        self.strategy = strategy
        self.batch_size = batch_size

    def validate_dimensions(self, records: list[EmbeddingRecord]) -> list[EmbeddingRecord]:
        """Filter out records with wrong dimensions."""
        expected = self.strategy.config.dimensions
        valid = [r for r in records if len(r.embedding) == expected]
        invalid = len(records) - len(valid)
        if invalid > 0:
            logger.warning(
                "Dropped %d records with wrong dimensions (expected %d)", invalid, expected
            )
        return valid

    def batch(self, records: list[EmbeddingRecord]) -> Iterator[list[EmbeddingRecord]]:
        """Yield records in batches."""
        for i in range(0, len(records), self.batch_size):
            yield records[i : i + self.batch_size]

    def build_insert_params(self, records: list[EmbeddingRecord]) -> list[Any]:
        """Build the parameter list for a batch insert."""
        params: list[Any] = []
        for record in records:
            params.append(record.id)
            vec_str = "[" + ", ".join(f"{v:.6f}" for v in record.embedding) + "]"
            params.append(vec_str)
        return params

    def load(self, records: list[EmbeddingRecord]) -> int:
        """Load a batch of embeddings. Returns number of rows inserted."""
        valid = self.validate_dimensions(records)
        total = 0
        for batch in self.batch(valid):
            sql = self.strategy.insert_sql(len(batch))
            _ = self.build_insert_params(batch)  # used in production
            # In production: execute(sql, params) via psycopg
            logger.info("Would insert %d rows: %s", len(batch), sql[:80])
            total += len(batch)
        return total
