"""PlanetScale Database Plugin"""
import os
from typing import Dict, List

class PlanetScaleClient:
    def __init__(self, token: str = None, org: str = None):
        self.token = token or os.environ.get("PLANETSCALE_TOKEN", "")
        self.org = org or os.environ.get("PLANETSCALE_ORG", "")
        self.base_url = "https://api.planetscale.com/v1"
    def _headers(self): return {"Authorization": f"{self.token}", "Content-Type": "application/json"}
    def list_databases(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/organizations/{self.org}/databases", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", [])
    def create_branch(self, db: str, branch: str, parent: str = "main") -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/organizations/{self.org}/databases/{db}/branches", headers=self._headers(), json={"name": branch, "parent_branch": parent}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_branches(self, db: str) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/organizations/{self.org}/databases/{db}/branches", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", [])

def register(plugin): plugin.set_resource("client_class", PlanetScaleClient)
planetscale_plugin = {"metadata": {"name": "planetscale", "version": "1.0.0", "description": "PlanetScale - Serverless MySQL", "author": "Mito Team", "license": "MIT", "tags": ["planetscale", "database", "mysql"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
