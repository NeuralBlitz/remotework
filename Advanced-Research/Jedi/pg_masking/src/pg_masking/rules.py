from __future__ import annotations

import hashlib
import re
from abc import ABC, abstractmethod
from typing import Any

from pg_masking.models import MaskingType


class Masker(ABC):
    """Base class for masking implementations."""

    def __init__(self, mask_char: str = "*") -> None:
        self.mask_char = mask_char

    @abstractmethod
    def mask(self, value: Any) -> str: ...


class RegexMasker(Masker):
    """Masks using a regex pattern, keeping captured groups visible."""

    def __init__(self, pattern: str, replacement: str | None = None, mask_char: str = "*") -> None:
        super().__init__(mask_char)
        self._pattern = re.compile(pattern)
        self._replacement = replacement

    def mask(self, value: Any) -> str:
        text = str(value)
        if self._replacement is not None:
            return self._pattern.sub(self._replacement, text)
        return self._pattern.sub(self.mask_char * 4, text)


class EmailMasker(Masker):
    """Masks email addresses: j***@example.com."""

    def mask(self, value: Any) -> str:
        text = str(value)
        match = re.match(r"^([^@])([^@]*)(@.+)$", text)
        if match:
            return f"{match.group(1)}{self.mask_char * 3}{match.group(3)}"
        if "@" in text:
            local, domain = text.split("@", 1)
            return f"{local[0]}{self.mask_char * 3}@{domain}"
        return self.mask_char * len(text)


class PhoneMasker(Masker):
    """Masks phone numbers: ***-***-1234 (keeps last 4 digits)."""

    def __init__(self, mask_char: str = "*") -> None:
        super().__init__(mask_char)
        self._digit_pattern = re.compile(r"\d")

    def mask(self, value: Any) -> str:
        text = str(value)
        digits = self._digit_pattern.findall(text)
        if len(digits) < 4:
            return self.mask_char * len(text)
        visible_digits = digits[-4:]
        result: list[str] = []
        vis_idx = len(visible_digits) - 1
        for ch in reversed(text):
            if ch.isdigit():
                if vis_idx >= 0:
                    result.append(visible_digits[vis_idx])
                    vis_idx -= 1
                else:
                    result.append(self.mask_char)
            else:
                result.append(ch)
        return "".join(reversed(result))


def create_masker(masking_type: MaskingType, mask_char: str = "*") -> Masker:
    """Factory for creating maskers from MaskingType."""
    if masking_type == MaskingType.FULL:
        return RegexMasker(pattern=".+", mask_char=mask_char)
    if masking_type == MaskingType.PARTIAL:
        return RegexMasker(pattern=r".(?=.{2})", mask_char=mask_char)
    if masking_type == MaskingType.HASH:
        return _HashMasker()
    if masking_type == MaskingType.REDACT:
        return _RedactMasker()
    raise ValueError(f"Unknown masking type: {masking_type}")


class _HashMasker(Masker):
    def mask(self, value: Any) -> str:
        return hashlib.sha256(str(value).encode()).hexdigest()[:12]


class _RedactMasker(Masker):
    def mask(self, value: Any) -> str:
        return "[REDACTED]"
