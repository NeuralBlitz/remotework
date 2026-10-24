from dataclasses import dataclass


@dataclass
class ImageSteg:
    image_path: str
    width: int
    height: int
    bit_depth: int

    def extract_lsb(self) -> list[int]:
        return [i % 2 for i in range(self.width * self.height)]

    def analyze_entropy(self) -> float:
        return 0.5


@dataclass
class DetectionResult:
    image: ImageSteg
    has_hidden_data: bool
    confidence: float
    method: str

    @property
    def is_suspicious(self) -> bool:
        return self.confidence > 0.7


def analyze_image(image: ImageSteg) -> DetectionResult:
    entropy = image.analyze_entropy()
    lsb = image.extract_lsb()
    chi_score = chi_square_test(lsb)
    confidence = min(1.0, chi_score / 10.0)
    return DetectionResult(image, confidence > 0.5, confidence, "chi_square")


def chi_square_test(data: list[int]) -> float:
    if not data:
        return 0.0
    expected = len(data) / 2
    chi_sq = sum((d - expected) ** 2 / expected for d in data if expected > 0)
    return chi_sq


def pixel_value_test(pixels: list[int]) -> float:
    if not pixels:
        return 0.0
    mean_val = sum(pixels) / len(pixels)
    variance = sum((p - mean_val) ** 2 for p in pixels) / len(pixels)
    return variance
