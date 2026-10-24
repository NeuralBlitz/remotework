from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ProteinSequence:
    sequence: str
    name: str = ""
    format: str = "fasta"

    @property
    def length(self) -> int:
        return len(self.sequence)

    @property
    def valid_amino_acids(self) -> bool:
        valid = set("ACDEFGHIKLMNPQRSTVWY")
        return all(c.upper() in valid for c in self.sequence)


@dataclass
class ProteinStructure:
    coordinates: list[tuple[float, float, float]] = field(default_factory=list)
    sequence: str = ""
    confidence: list[float] = field(default_factory=list)
    source_format: str = ""

    @property
    def num_residues(self) -> int:
        return len(self.coordinates)

    @property
    def mean_confidence(self) -> float:
        if not self.confidence:
            return 0.0
        return sum(self.confidence) / len(self.confidence)
