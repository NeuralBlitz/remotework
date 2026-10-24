"""Neon Serverless Postgres Plugin"""
import os
from typing import Dict, List

class NeonClient:
    def __init__(self, token: str = None):
        self.token = token or os.environ.get("NEON_TOKEN", "")
        self.base_url = "https://console.neon.tech/api/v2"
    def _headers(self): return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
    def list_projects(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/projects", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("projects", [])
    def create_project(self, name: str, region: str = "aws-us-east-1") -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/projects", headers=self._headers(), json={"project": {"name": name, "region_id": region}}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_branches(self, project_id: str) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/projects/{project_id}/branches", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("branches", [])

def register(plugin): plugin.set_resource("client_class", NeonClient)
neon_plugin = {"metadata": {"name": "neon", "version": "1.0.0", "description": "Neon - Serverless Postgres", "author": "Mito Team", "license": "MIT", "tags": ["neon", "postgres", "database", "serverless"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
