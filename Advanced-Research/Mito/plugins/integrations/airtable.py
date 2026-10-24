"""Airtable Plugin - Bases, tables, records via REST API"""
import os
from typing import Dict, List

class AirtableClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("AIRTABLE_API_KEY", "")
        self.base_url = "https://api.airtable.com/v0"
    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
    def list_records(self, base_id: str, table: str, max_records: int = 100) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/{base_id}/{table}", headers=self._headers(), params={"maxRecords": max_records}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("records", [])
    def create_record(self, base_id: str, table: str, fields: Dict) -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/{base_id}/{table}", headers=self._headers(), json={"fields": fields}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def update_record(self, base_id: str, table: str, record_id: str, fields: Dict) -> Dict:
        import requests
        resp = requests.patch(f"{self.base_url}/{base_id}/{table}/{record_id}", headers=self._headers(), json={"fields": fields}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def delete_record(self, base_id: str, table: str, record_id: str) -> bool:
        import requests
        resp = requests.delete(f"{self.base_url}/{base_id}/{table}/{record_id}", headers=self._headers(), timeout=30)
        return resp.ok

def register(plugin):
    plugin.set_resource("client_class", AirtableClient)

airtable_plugin = {"metadata": {"name": "airtable", "version": "1.0.0", "description": "Airtable - Bases, tables, records", "author": "Mito Team", "license": "MIT", "tags": ["airtable", "database", "spreadsheet"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
