"""
Cloudflare Plugin
DNS, zones, workers, KV via API
"""
import os
from typing import Dict, List

class CloudflareClient:
    def __init__(self, token: str = None, email: str = None, api_key: str = None):
        self.token = token or os.environ.get("CLOUDFLARE_TOKEN", "")
        self.email = email or os.environ.get("CLOUDFLARE_EMAIL", "")
        self.api_key = api_key or os.environ.get("CLOUDFLARE_API_KEY", "")
        self.base_url = "https://api.cloudflare.com/client/v4"

    def _headers(self) -> Dict[str, str]:
        if self.token:
            return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        return {"X-Auth-Email": self.email, "X-Auth-Key": self.api_key, "Content-Type": "application/json"}

    def list_zones(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/zones", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("result", [])

    def list_dns_records(self, zone_id: str) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/zones/{zone_id}/dns_records", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("result", [])

    def create_dns_record(self, zone_id: str, record_type: str, name: str, content: str, ttl: int = 1) -> Dict:
        import requests
        payload = {"type": record_type, "name": name, "content": content, "ttl": ttl}
        resp = requests.post(f"{self.base_url}/zones/{zone_id}/dns_records", headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json().get("result", {})

    def purge_cache(self, zone_id: str, purge_all: bool = True) -> Dict:
        import requests
        payload = {"purge_everything": purge_all}
        resp = requests.post(f"{self.base_url}/zones/{zone_id}/purge_cache", headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_workers(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/workers/scripts", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("result", [])

    def get_zone_analytics(self, zone_id: str, since: str = "-1") -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/zones/{zone_id}/analytics/dashboard", headers=self._headers(),
                             params={"since": since}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("result", {})

def register(plugin):
    plugin.set_resource("client_class", CloudflareClient)

cloudflare_plugin = {
    "metadata": {"name": "cloudflare", "version": "1.0.0", "description": "Cloudflare - DNS, zones, workers, cache",
                 "author": "Mito Team", "license": "MIT", "tags": ["cloudflare", "dns", "cdn", "workers"],
                 "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"},
    "register": register,
}
