from __future__ import annotations

from abc import ABC, abstractmethod

from protein_fold.models import ProteinSequence, ProteinStructure


class FormatAdapter(ABC):
    @abstractmethod
    def parse(self, raw: str) -> ProteinSequence: ...

    @abstractmethod
    def to_structure(self, seq: ProteinSequence) -> ProteinStructure: ...


class FastaAdapter(FormatAdapter):
    def parse(self, raw: str) -> ProteinSequence:
        lines = raw.strip().split("\n")
        name = lines[0].lstrip(">").strip() if lines else ""
        sequence = "".join(line.strip() for line in lines[1:] if not line.startswith(">"))
        return ProteinSequence(sequence=sequence.upper(), name=name, format="fasta")

    def to_structure(self, seq: ProteinSequence) -> ProteinStructure:
        coords = [(float(i), 0.0, 0.0) for i in range(seq.length)]
        conf = [0.7] * seq.length
        return ProteinStructure(
            coordinates=coords,
            sequence=seq.sequence,
            confidence=conf,
            source_format="fasta",
        )


class PDBAdapter(FormatAdapter):
    def parse(self, raw: str) -> ProteinSequence:
        seq_chars: list[str] = []
        name = ""
        for line in raw.strip().split("\n"):
            if line.startswith("HEADER"):
                name = line[10:].strip()
            elif line.startswith("ATOM") and line[13:15].strip() == "CA":
                residue = line[17:20].strip()
                one_letter = self._three_to_one(residue)
                if one_letter:
                    seq_chars.append(one_letter)
        return ProteinSequence(sequence="".join(seq_chars), name=name, format="pdb")

    def to_structure(self, seq: ProteinSequence) -> ProteinStructure:
        coords = [(float(i) * 3.8, 0.0, 0.0) for i in range(seq.length)]
        conf = [0.9] * seq.length
        return ProteinStructure(
            coordinates=coords,
            sequence=seq.sequence,
            confidence=conf,
            source_format="pdb",
        )

    @staticmethod
    def _three_to_one(residue: str) -> str:
        mapping = {
            "ALA": "A",
            "CYS": "C",
            "ASP": "D",
            "GLU": "E",
            "PHE": "F",
            "GLY": "G",
            "HIS": "H",
            "ILE": "I",
            "LYS": "K",
            "LEU": "L",
            "MET": "M",
            "ASN": "N",
            "PRO": "P",
            "GLN": "Q",
            "ARG": "R",
            "SER": "S",
            "THR": "T",
            "VAL": "V",
            "TRP": "W",
            "TYR": "Y",
        }
        return mapping.get(residue.upper(), "")
