"""Voyage AI Embeddings Plugin"""
import os
from typing import List
class VoyageClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("VOYAGE_API_KEY", "")
        self.base_url = "https://api.voyageai.com/v1"
    def _headers(self): return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
    def embed(self, texts: List[str], model: str = "voyage-3") -> List[List[float]]:
        import requests
        resp = requests.post(f"{self.base_url}/embeddings", headers=self._headers(), json={"input": texts, "model": model}, timeout=60)
        resp.raise_for_status()
        return [e["embedding"] for e in resp.json()["data"]]
def register(plugin): plugin.set_resource("client_class", VoyageClient)
voyage_plugin = {"metadata": {"name": "voyage", "version": "1.0.0", "description": "Voyage AI - High-quality embeddings", "author": "Mito Team", "license": "MIT", "tags": ["voyage", "embeddings", "ai"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
