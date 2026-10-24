from __future__ import annotations

from .models import AudioOutput, TextRequest


class TextNormalizer:
    def normalize(self, text: str) -> str:
        text = text.strip()
        replacements = {"Mr.": "Mister", "Dr.": "Doctor", "St.": "Street"}
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text


class PhonemeConverter:
    VOWELS = set("aeiou")

    def convert(self, text: str) -> list[str]:
        phonemes: list[str] = []
        for char in text.lower():
            if char.isalpha():
                if char in self.VOWELS:
                    phonemes.append(f"V({char})")
                else:
                    phonemes.append(f"C({char})")
            elif char == " ":
                phonemes.append("PAUSE")
        return phonemes


class AudioSynthesizer:
    def synthesize(self, phonemes: list[str], sample_rate: int = 22050) -> AudioOutput:
        duration_ms = len(phonemes) * 50
        return AudioOutput(
            duration_ms=duration_ms,
            sample_rate=sample_rate,
            phoneme_count=len(phonemes),
            raw_data=b"\x00" * (duration_ms * sample_rate // 1000),
        )


class TTSPipeline:
    def __init__(self, sample_rate: int = 22050) -> None:
        self.normalizer = TextNormalizer()
        self.converter = PhonemeConverter()
        self.synthesizer = AudioSynthesizer()
        self.sample_rate = sample_rate

    def run(self, request: TextRequest) -> AudioOutput:
        normalized = self.normalizer.normalize(request.text)
        phonemes = self.converter.convert(normalized)
        return self.synthesizer.synthesize(phonemes, self.sample_rate)

