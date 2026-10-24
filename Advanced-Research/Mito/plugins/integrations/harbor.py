"""Harbor Container Registry Plugin"""
import os
from typing import Dict, List

class HarborClient:
    def __init__(self, token: str = None, base_url: str = None):
        self.token = token or os.environ.get("HARBOR_PASSWORD", "")
        self.base_url = (base_url or os.environ.get("HARBOR_URL", "https://harbor.local")).rstrip("/")
    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
    def list_resources(self, resource: str = "items", limit: int = 50) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/{resource}", headers=self._headers(), params={"limit": limit}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else data.get("data", data.get("items", []))
    def get_resource(self, resource: str, id: str) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/{resource}/{id}", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def create_resource(self, resource: str, data: Dict) -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/{resource}", headers=self._headers(), json=data, timeout=30)
        resp.raise_for_status()
        return resp.json()

def register(plugin): plugin.set_resource("client_class", HarborClient)
harbor_plugin = {"metadata": {"name": "harbor", "version": "1.0.0", "description": "Harbor Container Registry", "author": "Mito Team", "license": "MIT", "tags": ["harbor", "integration"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
