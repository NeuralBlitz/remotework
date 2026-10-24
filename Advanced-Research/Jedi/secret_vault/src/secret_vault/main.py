"""Secret vault management."""
from __future__ import annotations

from .models import Secret

__all__ = ["Secret", "store_secret", "retrieve_secret"]

def store_secret(name: str, value: str) -> Secret:
    return Secret(name=name, encrypted_value=value)

def retrieve_secret(secret: Secret) -> str:
    return secret.decrypt()
