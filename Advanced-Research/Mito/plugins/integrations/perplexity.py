"""Perplexity AI Plugin"""
import os
from typing import Dict, List

class PerplexityClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("PERPLEXITY_API_KEY", "")
        self.base_url = "https://api.perplexity.ai"
    def _headers(self): return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
    def chat(self, messages: List[Dict], model: str = "llama-3.1-sonar-huge-128k-online") -> str:
        import requests
        resp = requests.post(f"{self.base_url}/chat/completions", headers=self._headers(), json={"model": model, "messages": messages}, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

def register(plugin): plugin.set_resource("client_class", PerplexityClient)
perplexity_plugin = {"metadata": {"name": "perplexity", "version": "1.0.0", "description": "Perplexity AI - Search-augmented LLM", "author": "Mito Team", "license": "MIT", "tags": ["perplexity", "ai", "search"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
