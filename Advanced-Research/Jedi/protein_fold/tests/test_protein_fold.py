from protein_fold.adapters import FastaAdapter, PDBAdapter
from protein_fold.models import ProteinSequence, ProteinStructure
from protein_fold.pipeline import FoldingPipeline


FASTA_DATA = ">seq1\nACDEFGHIKLMNPQRSTVWY"
PDB_DATA = "HEADER    EXAMPLE\nATOM      1  CA  ALA A   1       0.000   0.000   0.000\nATOM      2  CA  GLY A   2       3.800   0.000   0.000"


def test_fasta_adapter_parse() -> None:
    adapter = FastaAdapter()
    seq = adapter.parse(FASTA_DATA)
    assert seq.name == "seq1"
    assert seq.length == 20


def test_fasta_adapter_to_structure() -> None:
    adapter = FastaAdapter()
    seq = adapter.parse(FASTA_DATA)
    struct = adapter.to_structure(seq)
    assert struct.num_residues == 20
    assert struct.source_format == "fasta"


def test_pdb_adapter_parse() -> None:
    adapter = PDBAdapter()
    seq = adapter.parse(PDB_DATA)
    assert seq.length == 2
    assert seq.sequence == "AG"


def test_pdb_adapter_to_structure() -> None:
    adapter = PDBAdapter()
    seq = adapter.parse(PDB_DATA)
    struct = adapter.to_structure(seq)
    assert struct.num_residues == 2
    assert struct.source_format == "pdb"


def test_protein_sequence_valid_amino_acids() -> None:
    s = ProteinSequence("ACDEFGHIKLMNPQRSTVWY")
    assert s.valid_amino_acids
    s2 = ProteinSequence("ACDX")
    assert not s2.valid_amino_acids


def test_protein_structure_mean_confidence() -> None:
    s = ProteinStructure(confidence=[0.8, 0.9, 1.0])
    assert s.mean_confidence == pytest.approx(0.9)


def test_protein_structure_empty_confidence() -> None:
    s = ProteinStructure()
    assert s.mean_confidence == 0.0


def test_pipeline_detect_format() -> None:
    pipe = FoldingPipeline()
    assert pipe.detect_format(FASTA_DATA) == "fasta"
    assert pipe.detect_format(PDB_DATA) == "pdb"


def test_pipeline_fold_fasta() -> None:
    pipe = FoldingPipeline()
    pipe.register("fasta", FastaAdapter())
    struct = pipe.fold(FASTA_DATA)
    assert struct.num_residues == 20


def test_pipeline_fold_pdb() -> None:
    pipe = FoldingPipeline()
    pipe.register("pdb", PDBAdapter())
    struct = pipe.fold(PDB_DATA, fmt="pdb")
    assert struct.num_residues == 2


def test_pipeline_batch_fold() -> None:
    pipe = FoldingPipeline()
    pipe.register("fasta", FastaAdapter())
    results = pipe.batch_fold([FASTA_DATA, FASTA_DATA])
    assert len(results) == 2


import pytest
