"""GitLab Plugin - Projects, issues, merge requests via REST API"""
import os
from typing import Dict, List

class GitLabClient:
    def __init__(self, token: str = None, base_url: str = None):
        self.token = token or os.environ.get("GITLAB_TOKEN", "")
        self.base_url = (base_url or os.environ.get("GITLAB_URL", "https://gitlab.com/api/v4")).rstrip("/")
    def _headers(self) -> Dict[str, str]:
        return {"PRIVATE-TOKEN": self.token, "Content-Type": "application/json"}
    def list_projects(self, per_page: int = 20) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/projects", headers=self._headers(), params={"per_page": per_page, "membership": True}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def get_project(self, project_id: str) -> Dict:
        import requests
        resp = requests.get(f"{self.base_url}/projects/{project_id}", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_issues(self, project_id: str, state: str = "opened") -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/projects/{project_id}/issues", headers=self._headers(), params={"state": state}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def create_issue(self, project_id: str, title: str, description: str = "") -> Dict:
        import requests
        resp = requests.post(f"{self.base_url}/projects/{project_id}/issues", headers=self._headers(), json={"title": title, "description": description}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_mrs(self, project_id: str, state: str = "opened") -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/projects/{project_id}/merge_requests", headers=self._headers(), params={"state": state}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_commits(self, project_id: str, per_page: int = 20) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/projects/{project_id}/repository/commits", headers=self._headers(), params={"per_page": per_page}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    def list_pipelines(self, project_id: str) -> List[Dict]:
        import requests
        resp = requests.get(f"{self.base_url}/projects/{project_id}/pipelines", headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

def register(plugin):
    plugin.set_resource("client_class", GitLabClient)

gitlab_plugin = {"metadata": {"name": "gitlab", "version": "1.0.0", "description": "GitLab - Projects, issues, merge requests, pipelines", "author": "Mito Team", "license": "MIT", "tags": ["gitlab", "git", "ci-cd"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
