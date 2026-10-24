"""Auth0 Plugin - Users, roles, applications via Management API"""
import os
from typing import Dict, List

class Auth0Client:
    def __init__(self, domain: str = None, token: str = None):
        self.domain = domain or os.environ.get("AUTH0_DOMAIN", "")
        self.token = token or os.environ.get("AUTH0_TOKEN", "")
        self.base_url = f"https://{self.domain}/api/v2"
    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
    def list_users(self, per_page: int = 25) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/users", headers=self._headers(), params={"per_page": per_page}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def create_user(self, email: str, password: str, connection: str = "Username-Password-Authentication") -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/users", headers=self._headers(), json={"email": email, "password": password, "connection": connection}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def get_user(self, user_id: str) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/users/{user_id}", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_roles(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/roles", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def assign_role(self, user_id: str, role_ids: List[str]) -> bool:
        import requests
        resp = requests.post(f"{self.base_url}/users/{user_id}/roles", headers=self._headers(), json={"roles": role_ids}, timeout=30)
        return resp.ok

def register(plugin): plugin.set_resource("client_class", Auth0Client)

auth0_plugin = {"metadata": {"name": "auth0", "version": "1.0.0", "description": "Auth0 - Users, roles, applications", "author": "Mito Team", "license": "MIT", "tags": ["auth0", "auth", "identity"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
