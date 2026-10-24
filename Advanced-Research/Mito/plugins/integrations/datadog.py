"""
Datadog Monitoring Plugin
Metrics, events, monitors via API
"""
import os
from typing import Dict, List

class DatadogClient:
    def __init__(self, api_key: str = None, app_key: str = None):
        self.api_key = api_key or os.environ.get("DATADOG_API_KEY", "")
        self.app_key = app_key or os.environ.get("DATADOG_APP_KEY", "")
        self.base_url = "https://api.datadoghq.com/api/v1"

    def _headers(self) -> Dict[str, str]:
        return {"DD-API-KEY": self.api_key, "Content-Type": "application/json"}

    def submit_metric(self, metric: str, points: List, metric_type: str = "gauge", tags: List[str] = None) -> Dict:
        import requests
        payload = {"series": [{"metric": metric, "type": metric_type, "points": points, "tags": tags or []}]}
        resp = requests.post(f"{self.base_url}/series", headers=self._headers(), json=payload, timeout=10)
        return {"status": resp.status_code, "ok": resp.ok}

    def post_event(self, title: str, text: str, alert_type: str = "info", tags: List[str] = None) -> Dict:
        import requests
        payload = {"title": title, "text": text, "alert_type": alert_type, "tags": tags or []}
        resp = requests.post(f"{self.base_url}/events", headers=self._headers(), json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def list_monitors(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/monitor", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

def register(plugin):
    plugin.set_resource("client_class", DatadogClient)

datadog_plugin = {
    "metadata": {"name": "datadog", "version": "1.0.0", "description": "Datadog monitoring - Metrics, events, monitors",
                 "author": "Mito Team", "license": "MIT", "tags": ["datadog", "monitoring", "metrics"],
                 "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"},
    "register": register,
}
