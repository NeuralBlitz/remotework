"""
Zapier Integration Plugin
Trigger Zaps and receive webhook callbacks
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.zapier")


class ZapierClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ZAPIER_API_KEY", "")
        self.base_url = "https://zapier.com/api/v2"

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def trigger_webhook(self, webhook_url: str, data: Dict) -> Dict:
        import requests
        resp = requests.post(webhook_url, json=data, timeout=30)
        resp.raise_for_status()
        return {"status": resp.status_code, "triggered": True}

    def list_zaps(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/zaps", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", [])

    def enable_zap(self, zap_id: str) -> Dict:
        import requests
        resp = requests.patch(f"{self.base_url}/zaps/{zap_id}",
                               headers=self._headers(), json={"enabled": True}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def disable_zap(self, zap_id: str) -> Dict:
        import requests
        resp = requests.patch(f"{self.base_url}/zaps/{zap_id}",
                               headers=self._headers(), json={"enabled": False}, timeout=30)
        resp.raise_for_status()
        return resp.json()


def zapier_trigger_cmd(webhook_url: str = "", data: str = "{}") -> Dict:
    """Trigger a Zapier webhook."""
    client = ZapierClient()
    payload = json.loads(data) if isinstance(data, str) else data
    return client.trigger_webhook(webhook_url, payload)


def zapier_list_zaps_cmd() -> List[Dict]:
    """List all Zaps."""
    client = ZapierClient()
    return client.list_zaps()


def register(plugin):
    plugin.register_command("zapier_trigger", zapier_trigger_cmd)
    plugin.register_command("zapier_list_zaps", zapier_list_zaps_cmd)
    plugin.set_resource("client_class", ZapierClient)


PLUGIN_METADATA = {
    "name": "zapier",
    "version": "1.0.0",
    "description": "Zapier integration - Trigger Zaps, manage workflows",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["zapier", "automation", "workflows", "ifttt"],
    "dependencies": [],
    "permissions": ["network_access", "read_env"],
    "min_mito_version": "1.0.0",
}


zapier_plugin = {
    "metadata": PLUGIN_METADATA,
    "register": register,
}
