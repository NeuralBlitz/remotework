from dataclasses import dataclass


@dataclass
class GuideRNA:
    sequence: str
    pam: str = "NGG"

    def __post_init__(self) -> None:
        self.sequence = self.sequence.upper()


@dataclass
class PredictionResult:
    guide: GuideRNA
    efficiency: float
    off_target_score: float

    @property
    def is_viable(self) -> bool:
        return self.efficiency > 0.5 and self.off_target_score > 0.7


def predict_efficiency(guide: GuideRNA) -> PredictionResult:
    gc = gc_content(guide.sequence)
    efficiency = min(1.0, gc * 1.5) if 0.4 <= gc <= 0.6 else gc * 0.8
    off_target = 1.0 - (abs(gc - 0.5) * 2)
    return PredictionResult(guide, efficiency, off_target)


def gc_content(sequence: str) -> float:
    if not sequence:
        return 0.0
    return sum(1 for c in sequence.upper() if c in "GC") / len(sequence)


def find_pam_sites(dna: str, pam: str) -> list[int]:
    sites = []
    pam_len = len(pam)
    for i in range(len(dna) - pam_len + 1):
        if dna[i : i + pam_len].upper() == pam.upper():
            sites.append(i)
    return sites
