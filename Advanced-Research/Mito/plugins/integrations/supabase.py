"""
Supabase Plugin
Database, auth, storage, edge functions via REST API
"""
import os
from typing import Dict, List, Any

class SupabaseClient:
    def __init__(self, url: str = None, key: str = None):
        self.url = (url or os.environ.get("SUPABASE_URL", "")).rstrip("/")
        self.key = key or os.environ.get("SUPABASE_KEY", "")

    def _headers(self) -> Dict[str, str]:
        return {"apikey": self.key, "Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}

    def select(self, table: str, columns: str = "*", filters: Dict = None, limit: int = 100) -> List[Dict]:
        import requests
        params = {"select": columns, "limit": limit}
        if filters:
            for k, v in filters.items():
                params[f"{k}"] = f"eq.{v}"
        resp = requests.get(f"{self.url}/rest/v1/{table}", headers=self._headers(), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def insert(self, table: str, data: Dict) -> Dict:
        import requests
        resp = requests.post(f"{self.url}/rest/v1/{table}", headers=self._headers(), json=data,
                              params={"select": "*"}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def update(self, table: str, filters: Dict, data: Dict) -> List[Dict]:
        import requests
        params = {}
        for k, v in filters.items():
            params[f"{k}"] = f"eq.{v}"
        resp = requests.patch(f"{self.url}/rest/v1/{table}", headers=self._headers(), json=data,
                               params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def delete(self, table: str, filters: Dict) -> bool:
        import requests
        params = {}
        for k, v in filters.items():
            params[f"{k}"] = f"eq.{v}"
        resp = requests.delete(f"{self.url}/rest/v1/{table}", headers=self._headers(), params=params, timeout=30)
        return resp.ok

    def rpc(self, function_name: str, params: Dict = None) -> Any:
        import requests
        resp = requests.post(f"{self.url}/rest/v1/rpc/{function_name}", headers=self._headers(),
                              json=params or {}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def upload_storage(self, bucket: str, path: str, file_path: str, content_type: str = None) -> Dict:
        import requests
        headers = {**self._headers()}
        if content_type:
            headers["Content-Type"] = content_type
        with open(file_path, "rb") as f:
            resp = requests.post(f"{self.url}/storage/v1/object/{bucket}/{path}",
                                  headers=headers, data=f, timeout=60)
        resp.raise_for_status()
        return resp.json()

    def download_storage(self, bucket: str, path: str) -> bytes:
        import requests
        resp = requests.get(f"{self.url}/storage/v1/object/{bucket}/{path}",
                             headers=self._headers(), timeout=60)
        resp.raise_for_status()
        return resp.content

def register(plugin):
    plugin.set_resource("client_class", SupabaseClient)

supabase_plugin = {
    "metadata": {"name": "supabase", "version": "1.0.0", "description": "Supabase - Database, auth, storage, edge functions",
                 "author": "Mito Team", "license": "MIT", "tags": ["supabase", "database", "backend", "baas"],
                 "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"},
    "register": register,
}
