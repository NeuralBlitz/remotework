"""HuggingFace Hub Plugin"""
import os
from typing import Dict, List

class HuggingFaceClient:
    def __init__(self, token: str = None):
        self.token = token or os.environ.get("HF_TOKEN", "")
        self.base_url = "https://huggingface.co/api"
    def _headers(self):
        h = {}
        if self.token: h["Authorization"] = f"Bearer {self.token}"
        return h
    def search_models(self, query: str, limit: int = 20) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/models", params={"search": query, "limit": limit}, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def get_model(self, model_id: str) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/models/{model_id}", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_datasets(self, query: str = "", limit: int = 20) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/datasets", params={"search": query, "limit": limit}, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def inference(self, model: str, inputs: Dict) -> Dict:
        import requests
        resp = requests.post(f"https://api-inference.huggingface.co/models/{model}", headers=self._headers(), json=inputs, timeout=60)
        resp.raise_for_status()
        return resp.json()

def register(plugin): plugin.set_resource("client_class", HuggingFaceClient)
huggingface_plugin = {"metadata": {"name": "huggingface", "version": "1.0.0", "description": "HuggingFace Hub - Models, datasets, inference", "author": "Mito Team", "license": "MIT", "tags": ["huggingface", "ai", "ml", "models"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
