from stego_detect import DetectionResult, ImageSteg
from stego_detect.models import analyze_image, chi_square_test, pixel_value_test


class TestImageSteg:
    def test_creation(self) -> None:
        img = ImageSteg("test.png", 100, 100, 8)
        assert img.width == 100

    def test_extract_lsb(self) -> None:
        img = ImageSteg("test.png", 10, 10, 8)
        lsb = img.extract_lsb()
        assert len(lsb) == 100


class TestDetectionResult:
    def test_not_suspicious(self) -> None:
        img = ImageSteg("test.png", 10, 10, 8)
        result = DetectionResult(img, False, 0.5, "lsb")
        assert result.is_suspicious is False

    def test_suspicious(self) -> None:
        img = ImageSteg("test.png", 10, 10, 8)
        result = DetectionResult(img, True, 0.8, "chi_square")
        assert result.is_suspicious is True


class TestHelpers:
    def test_analyze_image(self) -> None:
        img = ImageSteg("test.png", 100, 100, 8)
        result = analyze_image(img)
        assert result.image == img

    def test_chi_square_test(self) -> None:
        data = [0, 1, 0, 1, 0, 1, 0, 1]
        score = chi_square_test(data)
        assert score >= 0

    def test_pixel_value_test(self) -> None:
        pixels = [100, 101, 99, 102, 100]
        result = pixel_value_test(pixels)
        assert result >= 0
