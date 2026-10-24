"""Clerk Plugin - Users, organizations via Backend API"""
import os
from typing import Dict, List

class ClerkClient:
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or os.environ.get("CLERK_SECRET_KEY", "")
        self.base_url = "https://api.clerk.com/v1"
    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.secret_key}", "Content-Type": "application/json"}
    def list_users(self, limit: int = 25) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/users", headers=self._headers(), params={"limit": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def create_user(self, email: str, password: str = None, first_name: str = None) -> Dict:
        import requests
        payload = {"email_address": [email]}
        if password: payload["password"] = password
        if first_name: payload["first_name"] = first_name
        resp = requests.post(f"{self.base_url}/users", headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def get_user(self, user_id: str) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/users/{user_id}", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def delete_user(self, user_id: str) -> bool:
        import requests
        resp = requests.delete(f"{self.base_url}/users/{user_id}", headers=self._headers(), timeout=30)
        return resp.ok
    def list_organizations(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/organizations", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", [])

def register(plugin): plugin.set_resource("client_class", ClerkClient)

clerk_plugin = {"metadata": {"name": "clerk", "version": "1.0.0", "description": "Clerk - Users, organizations, auth", "author": "Mito Team", "license": "MIT", "tags": ["clerk", "auth", "identity"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
