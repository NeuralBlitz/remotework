"""n8n Automation Plugin"""
import os
from typing import Dict, List

class N8NClient:
    def __init__(self, token: str = None, base_url: str = None):
        self.token = token or os.environ.get("N8N_TOKEN", "")
        self.base_url = (base_url or os.environ.get("N8N_URL", "")).rstrip("/")
    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
    def list(self, resource: str = "items", limit: int = 50) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/{resource}", headers=self._headers(), params={"limit": limit}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else data.get("data", data.get("items", []))
    def get(self, resource: str, id: str) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/{resource}/{id}", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def create(self, resource: str, data: Dict) -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/{resource}", headers=self._headers(), json=data, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def delete(self, resource: str, id: str) -> bool:
        import requests
        resp = requests.delete(f"{self.base_url}/{resource}/{id}", headers=self._headers(), timeout=30)
        return resp.ok

def register(plugin): plugin.set_resource("client_class", N8NClient)
n8n_plugin = {"metadata": {"name": "n8n", "version": "1.0.0", "description": "n8n workflow automation", "author": "Mito Team", "license": "MIT", "tags": ["n8n", "integration"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
