"""Asana Plugin - Projects, tasks, sections via REST API"""
import os
from typing import Dict, List

class AsanaClient:
    def __init__(self, token: str = None):
        self.token = token or os.environ.get("ASANA_TOKEN", "")
        self.base_url = "https://app.asana.com/api/1.0"
    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}
    def list_workspaces(self) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/workspaces", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", [])
    def list_projects(self, workspace: str) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/projects", headers=self._headers(), params={"workspace": workspace}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", [])
    def list_tasks(self, project: str, limit: int = 50) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/projects/{project}/tasks", headers=self._headers(), params={"limit": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", [])
    def create_task(self, workspace: str, name: str, projects: List[str] = None, assignee: str = None) -> Dict:
        import requests
        data = {"data": {"name": name, "workspace": workspace}}
        if projects:
            data["data"]["projects"] = projects
        if assignee:
            data["data"]["assignee"] = assignee
        resp = requests.post(f"{self.base_url}/tasks", headers=self._headers(), json=data, timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", {})
    def complete_task(self, task_id: str) -> Dict:
        import requests
        resp = requests.put(f"{self.base_url}/tasks/{task_id}", headers=self._headers(), json={"data": {"completed": True}}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", {})

def register(plugin):
    plugin.set_resource("client_class", AsanaClient)

asana_plugin = {"metadata": {"name": "asana", "version": "1.0.0", "description": "Asana - Projects, tasks, workspaces", "author": "Mito Team", "license": "MIT", "tags": ["asana", "project-management", "tasks"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
