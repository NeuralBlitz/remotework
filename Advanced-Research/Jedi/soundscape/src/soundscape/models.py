import math
from dataclasses import dataclass


@dataclass
class Layer:
    name: str
    frequency: float
    amplitude: float = 1.0
    duration: float = 10.0

    def generate_samples(self, sample_rate: int = 44100) -> list[float]:
        num_samples = int(self.duration * sample_rate)
        return [
            self.amplitude * math.sin(2 * math.pi * self.frequency * t / sample_rate)
            for t in range(num_samples)
        ]


@dataclass
class Sound:
    name: str
    layers: list[Layer]

    def mix(self) -> list[float]:
        if not self.layers:
            return []
        max_len = max(len(l.generate_samples()) for l in self.layers)
        mixed = [0.0] * max_len
        for layer in self.layers:
            samples = layer.generate_samples()
            for i, s in enumerate(samples):
                mixed[i] += s
        return mixed


def generate_ambient(name: str, base_freq: float = 220, num_layers: int = 4) -> Sound:
    layers = [
        Layer(f"layer_{i}", base_freq * (i + 1), 1.0 / (i + 1), 10.0) for i in range(num_layers)
    ]
    return Sound(name, layers)


def apply_fade(samples: list[float], fade_in: int = 0, fade_out: int = 0) -> list[float]:
    if not samples:
        return []
    faded = samples.copy()
    for i in range(fade_in):
        if i < len(faded):
            faded[i] *= i / fade_in if fade_in > 0 else 0
    for i in range(fade_out):
        idx = len(faded) - 1 - i
        if idx >= 0:
            faded[idx] *= i / fade_out if fade_out > 0 else 0
    return faded


def pitch_shift(samples: list[float], semitones: int) -> list[float]:
    factor = 2 ** (semitones / 12)
    new_len = int(len(samples) / factor)
    if new_len == 0:
        return []
    return samples[:new_len]
