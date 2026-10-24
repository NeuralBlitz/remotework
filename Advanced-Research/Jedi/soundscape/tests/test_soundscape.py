from soundscape import Layer, Sound
from soundscape.models import apply_fade, generate_ambient, pitch_shift


class TestLayer:
    def test_creation(self) -> None:
        l = Layer("bass", 60.0, 0.8, 5.0)
        assert l.frequency == 60.0

    def test_generate_samples(self) -> None:
        l = Layer("test", 440.0, 1.0, 0.1)
        samples = l.generate_samples(sample_rate=1000)
        assert len(samples) == 100


class TestSound:
    def test_mix_empty(self) -> None:
        s = Sound("empty", [])
        assert s.mix() == []

    def test_mix_layers(self) -> None:
        l1 = Layer("l1", 440.0, 0.5, 0.01)
        l2 = Layer("l2", 880.0, 0.5, 0.01)
        s = Sound("test", [l1, l2])
        mixed = s.mix()
        assert len(mixed) > 0


class TestHelpers:
    def test_generate_ambient(self) -> None:
        s = generate_ambient("test", base_freq=100, num_layers=3)
        assert len(s.layers) == 3

    def test_apply_fade(self) -> None:
        samples = [1.0] * 100
        faded = apply_fade(samples, fade_in=10, fade_out=10)
        assert len(faded) == 100

    def test_pitch_shift(self) -> None:
        samples = [1.0, 0.5, 0.0]
        shifted = pitch_shift(samples, semitones=12)
        assert len(shifted) == len(samples)
