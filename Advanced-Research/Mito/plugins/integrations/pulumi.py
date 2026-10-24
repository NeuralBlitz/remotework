"""Pulumi Cloud Plugin"""
import os
from typing import Dict, List

class PulumiClient:
    def __init__(self, token: str = None, org: str = None):
        self.token = token or os.environ.get("PULUMI_TOKEN", "")
        self.org = org or os.environ.get("PULUMI_ORG", "")
        self.base_url = "https://api.pulumi.com/api"
    def _headers(self): return {"Authorization": f"token {self.token}", "Content-Type": "application/json"}
    def list_stacks(self, project: str = None) -> List[Dict]:
        import requests
        url = f"{self.base_url}/user/stacks" if not self.org else f"{self.base_url}/orgs/{self.org}/stacks"
        resp = requests.get(url, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("stacks", [])

def register(plugin): plugin.set_resource("client_class", PulumiClient)
pulumi_plugin = {"metadata": {"name": "pulumi", "version": "1.0.0", "description": "Pulumi - Infrastructure as Code", "author": "Mito Team", "license": "MIT", "tags": ["pulumi", "iac", "cloud"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
