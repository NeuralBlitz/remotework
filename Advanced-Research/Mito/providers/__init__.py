"""
Mito LLM Providers
Unified interface for Mistral, Cohere, Groq, Together AI, Ollama, Fireworks
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Iterator
from dataclasses import dataclass

logger = logging.getLogger("mito.providers")


@dataclass
class ChatMessage:
    role: str
    content: str
    name: str = ""


class MistralProvider:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY", "")
        self.base_url = "https://api.mistral.ai/v1"

    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def chat(self, messages: List[Dict], model: str = "mistral-medium-latest", **kwargs) -> str:
        import requests
        resp = requests.post(f"{self.base_url}/chat/completions", headers=self._headers(),
                              json={"model": model, "messages": messages, **kwargs}, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def list_models(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/models", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()["data"]

    def embed(self, texts: List[str], model: str = "mistral-embed") -> List[List[float]]:
        import requests
        resp = requests.post(f"{self.base_url}/embeddings", headers=self._headers(),
                              json={"model": model, "input": texts}, timeout=60)
        resp.raise_for_status()
        return [e["embedding"] for e in resp.json()["data"]]


class CohereProvider:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("COHERE_API_KEY", "")
        self.base_url = "https://api.cohere.ai/v1"

    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def chat(self, messages: List[Dict], model: str = "command-r-plus", **kwargs) -> str:
        import requests
        resp = requests.post(f"{self.base_url}/chat", headers=self._headers(),
                              json={"model": model, "chat_history": messages[:-1],
                                    "message": messages[-1]["content"], **kwargs}, timeout=60)
        resp.raise_for_status()
        return resp.json()["text"]

    def embed(self, texts: List[str], model: str = "embed-english-v3.0", input_type: str = "search_document") -> List[List[float]]:
        import requests
        resp = requests.post(f"{self.base_url}/embed", headers=self._headers(),
                              json={"model": model, "texts": texts, "input_type": input_type}, timeout=60)
        resp.raise_for_status()
        return resp.json()["embeddings"]

    def rerank(self, query: str, documents: List[str], top_n: int = 5) -> List[Dict]:
        import requests
        resp = requests.post(f"{self.base_url}/rerank", headers=self._headers(),
                              json={"query": query, "documents": documents, "top_n": top_n}, timeout=30)
        resp.raise_for_status()
        return resp.json()["results"]

    def classify(self, inputs: List[str], model: str = "embed-english-v3.0") -> List[Dict]:
        import requests
        resp = requests.post(f"{self.base_url}/classify", headers=self._headers(),
                              json={"inputs": inputs, "model": model}, timeout=30)
        resp.raise_for_status()
        return resp.json()["classifications"]


class GroqProvider:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY", "")
        self.base_url = "https://api.groq.com/openai/v1"

    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def chat(self, messages: List[Dict], model: str = "llama-3.1-70b-versatile", **kwargs) -> str:
        import requests
        resp = requests.post(f"{self.base_url}/chat/completions", headers=self._headers(),
                              json={"model": model, "messages": messages, **kwargs}, timeout=30)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def chat_stream(self, messages: List[Dict], model: str = "llama-3.1-70b-versatile", **kwargs) -> Iterator[str]:
        import requests
        resp = requests.post(f"{self.base_url}/chat/completions", headers=self._headers(),
                              json={"model": model, "messages": messages, "stream": True, **kwargs},
                              stream=True, timeout=60)
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


class TogetherProvider:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("TOGETHER_API_KEY", "")
        self.base_url = "https://api.together.xyz/v1"

    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def chat(self, messages: List[Dict], model: str = "meta-llama/Llama-3-70b-chat-hf", **kwargs) -> str:
        import requests
        resp = requests.post(f"{self.base_url}/chat/completions", headers=self._headers(),
                              json={"model": model, "messages": messages, **kwargs}, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def complete(self, prompt: str, model: str = "meta-llama/Llama-3-70b-chat-hf", **kwargs) -> str:
        import requests
        resp = requests.post(f"{self.base_url}/completions", headers=self._headers(),
                              json={"model": model, "prompt": prompt, **kwargs}, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["text"]


class OllamaProvider:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.environ.get("OLLAMA_HOST", "http://localhost:11434")

    def chat(self, messages: List[Dict], model: str = "llama3.1", **kwargs) -> str:
        import requests
        resp = requests.post(f"{self.base_url}/api/chat",
                              json={"model": model, "messages": messages, "stream": False, **kwargs},
                              timeout=120)
        resp.raise_for_status()
        return resp.json()["message"]["content"]

    def chat_stream(self, messages: List[Dict], model: str = "llama3.1", **kwargs) -> Iterator[str]:
        import requests
        resp = requests.post(f"{self.base_url}/api/chat",
                              json={"model": model, "messages": messages, "stream": True, **kwargs},
                              stream=True, timeout=120)
        resp.raise_for_status()
        for line in resp.iter_lines():
            if line:
                chunk = json.loads(line)
                if "message" in chunk and "content" in chunk["message"]:
                    yield chunk["message"]["content"]

    def generate(self, prompt: str, model: str = "llama3.1", **kwargs) -> str:
        import requests
        resp = requests.post(f"{self.base_url}/api/generate",
                              json={"model": model, "prompt": prompt, "stream": False, **kwargs},
                              timeout=120)
        resp.raise_for_status()
        return resp.json()["response"]

    def embed(self, text: str, model: str = "llama3.1") -> List[float]:
        import requests
        resp = requests.post(f"{self.base_url}/api/embeddings",
                              json={"model": model, "prompt": text}, timeout=60)
        resp.raise_for_status()
        return resp.json()["embedding"]

    def list_models(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/api/tags", timeout=10)
        resp.raise_for_status()
        return resp.json().get("models", [])

    def pull_model(self, model: str) -> bool:
        import requests
        resp = requests.post(f"{self.base_url}/api/pull",
                              json={"name": model, "stream": False}, timeout=600)
        return resp.ok


class FireworksProvider:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("FIREWORKS_API_KEY", "")
        self.base_url = "https://api.fireworks.ai/inference/v1"

    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def chat(self, messages: List[Dict], model: str = "accounts/fireworks/models/llama-v3p1-70b-instruct", **kwargs) -> str:
        import requests
        resp = requests.post(f"{self.base_url}/chat/completions", headers=self._headers(),
                              json={"model": model, "messages": messages, **kwargs}, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


class LLMRouter:
    """Route requests to the best available provider."""

    def __init__(self):
        self.providers = {
            "openai": None, "anthropic": None, "mistral": None,
            "cohere": None, "groq": None, "together": None,
            "ollama": None, "fireworks": None,
        }
        self._load_providers()

    def _load_providers(self):
        try: from plugins.integrations.llm_gateway import OpenAIClient; self.providers["openai"] = OpenAIClient()
        except: pass
        try: from plugins.integrations.llm_gateway import AnthropicClient; self.providers["anthropic"] = AnthropicClient()
        except: pass
        if os.environ.get("MISTRAL_API_KEY"):
            self.providers["mistral"] = MistralProvider()
        if os.environ.get("COHERE_API_KEY"):
            self.providers["cohere"] = CohereProvider()
        if os.environ.get("GROQ_API_KEY"):
            self.providers["groq"] = GroqProvider()
        if os.environ.get("TOGETHER_API_KEY"):
            self.providers["together"] = TogetherProvider()
        self.providers["ollama"] = OllamaProvider()
        if os.environ.get("FIREWORKS_API_KEY"):
            self.providers["fireworks"] = FireworksProvider()

    def chat(self, messages: List[Dict], provider: str = None, model: str = None, **kwargs) -> str:
        p = provider or self._auto_select()
        prov = self.providers.get(p)
        if not prov:
            raise ValueError(f"Provider '{p}' not available")
        return prov.chat(messages, model=model, **kwargs)

    def _auto_select(self) -> str:
        for name in ["groq", "openai", "anthropic", "mistral", "ollama"]:
            if self.providers.get(name):
                return name
        raise ValueError("No LLM provider available")

    def available_providers(self) -> List[str]:
        return [k for k, v in self.providers.items() if v is not None]
