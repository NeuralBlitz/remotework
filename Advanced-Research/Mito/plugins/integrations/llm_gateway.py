"""
LLM Gateway Plugin
Unified interface for OpenAI, Anthropic Claude, and other LLM APIs
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Iterator

logger = logging.getLogger("mito.plugins.llm_gateway")


class OpenAIClient:
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = base_url

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def chat(self, messages: List[Dict], model: str = "gpt-4o", temperature: float = 0.7,
             max_tokens: int = 1024, stream: bool = False) -> Dict:
        import requests
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }
        resp = requests.post(f"{self.base_url}/chat/completions",
                              headers=self._headers(), json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()

    def chat_stream(self, messages: List[Dict], model: str = "gpt-4o",
                    temperature: float = 0.7, max_tokens: int = 1024) -> Iterator[str]:
        import requests
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        resp = requests.post(f"{self.base_url}/chat/completions",
                              headers=self._headers(), json=payload, stream=True, timeout=120)
        resp.raise_for_status()
        for line in resp.iter_lines():
            if line and line.startswith(b"data: "):
                data = line[6:]
                if data == b"[DONE]":
                    break
                chunk = json.loads(data)
                delta = chunk["choices"][0].get("delta", {})
                if "content" in delta:
                    yield delta["content"]

    def embed(self, texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
        import requests
        payload = {"model": model, "input": texts}
        resp = requests.post(f"{self.base_url}/embeddings",
                              headers=self._headers(), json=payload, timeout=60)
        resp.raise_for_status()
        return [item["embedding"] for item in resp.json()["data"]]

    def list_models(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/models", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()["data"]


class AnthropicClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.base_url = "https://api.anthropic.com/v1"
        self.version = "2023-06-01"

    def _headers(self) -> Dict[str, str]:
        return {
            "x-api-key": self.api_key,
            "anthropic-version": self.version,
            "Content-Type": "application/json",
        }

    def chat(self, messages: List[Dict], model: str = "claude-sonnet-4-20250514",
             max_tokens: int = 1024, system: str = "", temperature: float = 0.7) -> Dict:
        import requests
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature,
        }
        if system:
            payload["system"] = system
        resp = requests.post(f"{self.base_url}/messages",
                              headers=self._headers(), json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()

    def chat_stream(self, messages: List[Dict], model: str = "claude-sonnet-4-20250514",
                    max_tokens: int = 1024, system: str = "") -> Iterator[str]:
        import requests
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
            "stream": True,
        }
        if system:
            payload["system"] = system
        resp = requests.post(f"{self.base_url}/messages",
                              headers=self._headers(), json=payload, stream=True, timeout=120)
        resp.raise_for_status()
        for line in resp.iter_lines():
            if line and line.startswith(b"data: "):
                data = line[6:]
                chunk = json.loads(data)
                if chunk.get("type") == "content_block_delta":
                    yield chunk.get("delta", {}).get("text", "")


class LLMGateway:
    """Unified interface across providers."""

    def __init__(self):
        self.openai = OpenAIClient()
        self.anthropic = AnthropicClient()

    def chat(self, messages: List[Dict], provider: str = "openai", model: str = None,
             **kwargs) -> str:
        if provider == "openai":
            resp = self.openai.chat(messages, model=model or "gpt-4o", **kwargs)
            return resp["choices"][0]["message"]["content"]
        elif provider == "anthropic":
            resp = self.anthropic.chat(messages, model=model or "claude-sonnet-4-20250514", **kwargs)
            return resp["content"][0]["text"]
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def chat_stream(self, messages: List[Dict], provider: str = "openai",
                    model: str = None, **kwargs) -> Iterator[str]:
        if provider == "openai":
            yield from self.openai.chat_stream(messages, model=model or "gpt-4o", **kwargs)
        elif provider == "anthropic":
            yield from self.anthropic.chat_stream(messages, model=model or "claude-sonnet-4-20250514", **kwargs)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def embed(self, texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
        return self.openai.embed(texts, model=model)

    def complete(self, prompt: str, provider: str = "openai", model: str = None,
                 system: str = "", **kwargs) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return self.chat(messages, provider=provider, model=model, **kwargs)


def llm_chat_cmd(prompt: str = "", provider: str = "openai", model: str = "") -> str:
    """Chat with an LLM (OpenAI or Anthropic)."""
    gateway = LLMGateway()
    return gateway.complete(prompt, provider=provider, model=model or None)


def llm_embed_cmd(texts: str = "") -> List[List[float]]:
    """Generate embeddings via OpenAI."""
    gateway = LLMGateway()
    items = [t.strip() for t in texts.split("|||") if t.strip()]
    return gateway.embed(items)


def register(plugin):
    plugin.register_command("llm_chat", llm_chat_cmd)
    plugin.register_command("llm_embed", llm_embed_cmd)
    plugin.set_resource("gateway_class", LLMGateway)
    plugin.set_resource("openai_class", OpenAIClient)
    plugin.set_resource("anthropic_class", AnthropicClient)


PLUGIN_METADATA = {
    "name": "llm_gateway",
    "version": "1.0.0",
    "description": "LLM Gateway - OpenAI GPT-4, Anthropic Claude, embeddings",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["llm", "openai", "anthropic", "claude", "gpt", "embeddings"],
    "dependencies": [],
    "permissions": ["network_access", "read_env"],
    "min_mito_version": "1.0.0",
}


llm_gateway_plugin = {
    "metadata": PLUGIN_METADATA,
    "register": register,
}
