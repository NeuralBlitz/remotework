"""
Jira Integration Plugin
Issues, projects, sprints via Jira REST API
"""

import os
import json
import base64
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.jira")


class JiraClient:
    def __init__(self, base_url: Optional[str] = None, email: Optional[str] = None,
                 api_token: Optional[str] = None):
        self.base_url = (base_url or os.environ.get("JIRA_URL", "")).rstrip("/")
        self.email = email or os.environ.get("JIRA_EMAIL", "")
        self.api_token = api_token or os.environ.get("JIRA_API_TOKEN", "")

    def _headers(self) -> Dict[str, str]:
        creds = base64.b64encode(f"{self.email}:{self.api_token}".encode()).decode()
        return {
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _request(self, method: str, path: str, data: Dict = None, params: Dict = None) -> Any:
        import requests
        url = f"{self.base_url}/rest/api/3{path}"
        resp = requests.request(method, url, headers=self._headers(), json=data, params=params, timeout=30)
        resp.raise_for_status()
        if resp.status_code == 204:
            return {"ok": True}
        return resp.json()

    def get_issue(self, issue_key: str, fields: str = None) -> Dict:
        params = {}
        if fields:
            params["fields"] = fields
        return self._request("GET", f"/issue/{issue_key}", params=params)

    def create_issue(self, project_key: str, summary: str, issue_type: str = "Task",
                     description: str = "", assignee: str = None, labels: List[str] = None,
                     priority: str = None) -> Dict:
        fields = {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": issue_type},
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]
            },
        }
        if assignee:
            fields["assignee"] = {"accountId": assignee}
        if labels:
            fields["labels"] = labels
        if priority:
            fields["priority"] = {"name": priority}
        return self._request("POST", "/issue", {"fields": fields})

    def update_issue(self, issue_key: str, fields: Dict) -> Dict:
        return self._request("PUT", f"/issue/{issue_key}", {"fields": fields})

    def transition_issue(self, issue_key: str, transition_id: str) -> Dict:
        return self._request("POST", f"/issue/{issue_key}/transitions",
                              {"transition": {"id": transition_id}})

    def search_issues(self, jql: str, max_results: int = 50, fields: str = "*navigable") -> List[Dict]:
        result = self._request("POST", "/search", {
            "jql": jql,
            "maxResults": max_results,
            "fields": fields.split(","),
        })
        return result.get("issues", [])

    def get_projects(self) -> List[Dict]:
        return self._request("GET", "/project")

    def get_board(self, board_id: int) -> Dict:
        import requests
        url = f"{self.base_url}/rest/agile/1.0/board/{board_id}"
        resp = requests.get(url, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_sprints(self, board_id: int, state: str = "active") -> List[Dict]:
        import requests
        url = f"{self.base_url}/rest/agile/1.0/board/{board_id}/sprint"
        params = {"state": state}
        resp = requests.get(url, headers=self._headers(), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("values", [])

    def add_comment(self, issue_key: str, body: str) -> Dict:
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": body}]}]
            }
        }
        return self._request("POST", f"/issue/{issue_key}/comment", payload)


def jira_get_issue_cmd(issue_key: str = "") -> Dict:
    """Get a Jira issue by key."""
    client = JiraClient()
    return client.get_issue(issue_key)


def jira_create_issue_cmd(project_key: str = "", summary: str = "", issue_type: str = "Task") -> Dict:
    """Create a new Jira issue."""
    client = JiraClient()
    return client.create_issue(project_key, summary, issue_type)


def jira_search_cmd(jql: str = "", max_results: int = 50) -> List[Dict]:
    """Search Jira issues with JQL."""
    client = JiraClient()
    return client.search_issues(jql, max_results=max_results)


def jira_get_projects_cmd() -> List[Dict]:
    """List all Jira projects."""
    client = JiraClient()
    return client.get_projects()


def register(plugin):
    plugin.register_command("jira_get_issue", jira_get_issue_cmd)
    plugin.register_command("jira_create_issue", jira_create_issue_cmd)
    plugin.register_command("jira_search", jira_search_cmd)
    plugin.register_command("jira_get_projects", jira_get_projects_cmd)
    plugin.set_resource("client_class", JiraClient)


PLUGIN_METADATA = {
    "name": "jira",
    "version": "1.0.0",
    "description": "Jira integration - Issues, projects, sprints, JQL search",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["jira", "issues", "projects", "agile", "sprints"],
    "dependencies": [],
    "permissions": ["network_access", "read_env"],
    "min_mito_version": "1.0.0",
}


jira_plugin = {
    "metadata": PLUGIN_METADATA,
    "register": register,
}
