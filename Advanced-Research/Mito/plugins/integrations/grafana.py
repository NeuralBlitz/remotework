"""Grafana Plugin"""
import os
from typing import Dict, List

class GrafanaClient:
    def __init__(self, url: str = None, token: str = None):
        self.url = (url or os.environ.get("GRAFANA_URL", "http://localhost:3000")).rstrip("/")
        self.token = token or os.environ.get("GRAFANA_TOKEN", "")
    def _headers(self): return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
    def list_dashboards(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.url}/api/search", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def get_dashboard(self, uid: str) -> Dict:
        import requests
        resp = requests.get(f"{self.url}/api/dashboards/uid/{uid}", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def create_annotation(self, dashboard_id: int, text: str, tags: List[str] = None) -> Dict:
        import requests
        resp = requests.post(f"{self.url}/api/annotations", headers=self._headers(), json={"dashboardId": dashboard_id, "text": text, "tags": tags or []}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_alerts(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.url}/api/alerts", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

def register(plugin): plugin.set_resource("client_class", GrafanaClient)
grafana_plugin = {"metadata": {"name": "grafana", "version": "1.0.0", "description": "Grafana dashboards and alerts", "author": "Mito Team", "license": "MIT", "tags": ["grafana", "monitoring", "dashboards"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
