from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class HEScheme(Enum):
    CKKS = "ckks"
    BFV = "bfv"
    BGW = "bgw"


@dataclass
class HEConfig:
    scheme: HEScheme = HEScheme.CKKS
    poly_modulus_degree: int = 8192
    security_level: int = 128
    scale: float = 2**40
    num_slots: int = 4096
    max_depth: int = 5

    def validate(self) -> bool:
        if self.poly_modulus_degree not in [4096, 8192, 16384, 32768]:
            return False
        if self.security_level not in [128, 192, 256]:
            return False
        return self.max_depth > 0


@dataclass
class EncryptedTensor:
    ciphertext: bytes = b""
    shape: tuple[int, ...] = ()
    scale: float = 1.0
    is_encrypted: bool = True

    def size(self) -> int:
        result = 1
        for dim in self.shape:
            result *= dim
        return result

    def is_valid(self) -> bool:
        return len(self.ciphertext) > 0 and len(self.shape) > 0
