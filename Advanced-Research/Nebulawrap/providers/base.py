# nebulawrap/providers/base.py
from abc import ABC, abstractmethod

class ProviderAdapter(ABC):
    @abstractmethod
    def info(self) -> dict:
        """Return provider/model features and costs."""
        pass

    @abstractmethod
    async def generate(self, prompt: str, **opts) -> dict:
        """Sync/async generate -> returns {'text':..., 'usage':{}}"""
        pass

    @abstractmethod
    async def stream(self, prompt: str, on_token, **opts):
        """Stream tokens; call on_token(token) as chunks arrive."""
        pass
