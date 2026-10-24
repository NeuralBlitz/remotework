"""Terraform Cloud Plugin"""
import os
from typing import Dict, List

class TerraformCloudClient:
    def __init__(self, token: str = None, org: str = None):
        self.token = token or os.environ.get("TFE_TOKEN", "")
        self.org = org or os.environ.get("TFE_ORG", "")
        self.base_url = "https://app.terraform.io/api/v2"
    def _headers(self): return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/vnd.api+json"}
    def list_workspaces(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/organizations/{self.org}/workspaces", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", [])
    def create_run(self, workspace_id: str, message: str = "Triggered by Mito") -> Dict:
        import requests
        payload = {"data": {"type": "runs", "attributes": {"message": message}, "relationships": {"workspace": {"data": {"type": "workspaces", "id": workspace_id}}}}}
        resp = requests.post(f"{self.base_url}/runs", headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_runs(self, workspace_id: str) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/workspaces/{workspace_id}/runs", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", [])

def register(plugin): plugin.set_resource("client_class", TerraformCloudClient)
terraform_cloud_plugin = {"metadata": {"name": "terraform_cloud", "version": "1.0.0", "description": "Terraform Cloud - Workspaces, runs", "author": "Mito Team", "license": "MIT", "tags": ["terraform", "iac", "devops"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
