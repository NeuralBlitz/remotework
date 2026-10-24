"""Replicate AI Platform Plugin"""
import os
from typing import Dict, List

class ReplicateClient:
    def __init__(self, token: str = None):
        self.token = token or os.environ.get("REPLICATE_API_TOKEN", "")
        self.base_url = "https://api.replicate.com/v1"
    def _headers(self): return {"Authorization": f"Token {self.token}", "Content-Type": "application/json"}
    def run_model(self, model: str, input_data: Dict) -> Dict:
        import requests
        owner, name = model.split("/")
        resp = requests.post(f"{self.base_url}/models/{owner}/{name}/predictions", headers=self._headers(), json={"input": input_data}, timeout=120)
        resp.raise_for_status()
        return resp.json()
    def get_prediction(self, prediction_id: str) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/predictions/{prediction_id}", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_models(self, query: str = "") -> List[Dict]:
        import requests
        params = {"query": query} if query else {}
        resp = requests.get(f"{self.base_url}/models", headers=self._headers(), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("results", [])

def register(plugin): plugin.set_resource("client_class", ReplicateClient)
replicate_plugin = {"metadata": {"name": "replicate", "version": "1.0.0", "description": "Replicate AI platform - Run models via API", "author": "Mito Team", "license": "MIT", "tags": ["replicate", "ai", "ml"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
