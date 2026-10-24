"""
PagerDuty Incidents Plugin
Incidents, services, on-call via API v2
"""
import os
from typing import Dict, List

class PagerDutyClient:
    def __init__(self, token: str = None):
        self.token = token or os.environ.get("PAGERDUTY_TOKEN", "")
        self.base_url = "https://api.pagerduty.com"

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Token token={self.token}", "Content-Type": "application/json"}

    def create_incident(self, service_id: str, title: str, urgency: str = "high") -> Dict:
        import requests
        payload = {"incident": {"type": "incident", "title": title, "service": {"id": service_id, "type": "service_reference"}, "urgency": urgency}}
        resp = requests.post(f"{self.base_url}/incidents", headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_incidents(self, statuses: List[str] = None, limit: int = 25) -> List[Dict]:
        import requests
        params = {"limit": limit}
        if statuses:
            params["statuses[]"] = statuses
        resp = requests.get(f"{self.base_url}/incidents", headers=self._headers(), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("incidents", [])

    def acknowledge_incident(self, incident_id: str) -> Dict:
        import requests
        resp = requests.put(f"{self.base_url}/incidents/{incident_id}", headers=self._headers(),
                             json={"incident": {"type": "incident_reference", "status": "acknowledged"}}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def resolve_incident(self, incident_id: str) -> Dict:
        import requests
        resp = requests.put(f"{self.base_url}/incidents/{incident_id}", headers=self._headers(),
                             json={"incident": {"type": "incident_reference", "status": "resolved"}}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_oncall(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/oncalls", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("oncalls", [])

    def list_services(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/services", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("services", [])

def register(plugin):
    plugin.set_resource("client_class", PagerDutyClient)

pagerduty_plugin = {
    "metadata": {"name": "pagerduty", "version": "1.0.0", "description": "PagerDuty - Incidents, services, on-call",
                 "author": "Mito Team", "license": "MIT", "tags": ["pagerduty", "incidents", "oncall"],
                 "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"},
    "register": register,
}
