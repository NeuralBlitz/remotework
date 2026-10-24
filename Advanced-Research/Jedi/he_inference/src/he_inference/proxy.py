from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod

from he_inference.models import EncryptedTensor, HEConfig, HEScheme


class HEInterface(ABC):
    @abstractmethod
    def encrypt(self, data: list[float], config: HEConfig) -> EncryptedTensor: ...

    @abstractmethod
    def decrypt(self, tensor: EncryptedTensor, config: HEConfig) -> list[float]: ...

    @abstractmethod
    def evaluate(self, tensor: EncryptedTensor, operation: str) -> EncryptedTensor: ...


class HEProxy(HEInterface):
    def __init__(self) -> None:
        self._call_count = 0
        self._cache: dict[str, EncryptedTensor] = {}

    def encrypt(self, data: list[float], config: HEConfig) -> EncryptedTensor:
        if not config.validate():
            raise ValueError("Invalid HE config")
        self._call_count += 1
        raw = str(data).encode()
        ct = hashlib.sha256(raw).digest()
        return EncryptedTensor(
            ciphertext=ct * (config.poly_modulus_degree // 32),
            shape=(len(data),),
            scale=config.scale,
        )

    def decrypt(self, tensor: EncryptedTensor, config: HEConfig) -> list[float]:
        if not tensor.is_valid():
            raise ValueError("Invalid encrypted tensor")
        return [float(len(tensor.ciphertext)) * 1e-10] * tensor.size()

    def evaluate(self, tensor: EncryptedTensor, operation: str) -> EncryptedTensor:
        key = f"{tensor.ciphertext[:16].hex()}_{operation}"
        if key in self._cache:
            return self._cache[key]
        result = EncryptedTensor(
            ciphertext=tensor.ciphertext,
            shape=tensor.shape,
            scale=tensor.scale * 2 if operation == "square" else tensor.scale,
        )
        self._cache[key] = result
        return result

    @property
    def call_count(self) -> int:
        return self._call_count


class CKKSProxy(HEProxy):
    def __init__(self) -> None:
        super().__init__()
        self._rescale_count = 0

    def encrypt(self, data: list[float], config: HEConfig) -> EncryptedTensor:
        config.scheme = HEScheme.CKKS
        result = super().encrypt(data, config)
        self._rescale_count += 1
        return result

    def rescale(self, tensor: EncryptedTensor) -> EncryptedTensor:
        self._rescale_count += 1
        return EncryptedTensor(
            ciphertext=tensor.ciphertext,
            shape=tensor.shape,
            scale=tensor.scale / 2.0,
            is_encrypted=True,
        )

    @property
    def rescale_count(self) -> int:
        return self._rescale_count
