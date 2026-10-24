from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Secret:
    name: str
    encrypted_value: str

    def decrypt(self) -> str:
        return "decrypted"
