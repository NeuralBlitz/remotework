from __future__ import annotations

from protein_fold.adapters import FormatAdapter
from protein_fold.models import ProteinSequence, ProteinStructure


class FoldingPipeline:
    def __init__(self) -> None:
        self._adapters: dict[str, FormatAdapter] = {}

    def register(self, fmt: str, adapter: FormatAdapter) -> None:
        self._adapters[fmt.lower()] = adapter

    def detect_format(self, raw: str) -> str:
        if raw.strip().startswith(">"):
            return "fasta"
        if raw.strip().startswith("HEADER") or "ATOM" in raw:
            return "pdb"
        return "fasta"

    def parse(self, raw: str, fmt: str | None = None) -> ProteinSequence:
        if fmt is None:
            fmt = self.detect_format(raw)
        adapter = self._adapters.get(fmt.lower())
        if adapter is None:
            raise ValueError(f"No adapter registered for format: {fmt}")
        return adapter.parse(raw)

    def fold(self, raw: str, fmt: str | None = None) -> ProteinStructure:
        seq = self.parse(raw, fmt)
        adapter = self._adapters.get(seq.format)
        if adapter is None:
            raise ValueError(f"No adapter for format: {seq.format}")
        return adapter.to_structure(seq)

    def batch_fold(self, inputs: list[str]) -> list[ProteinStructure]:
        return [self.fold(raw) for raw in inputs]
