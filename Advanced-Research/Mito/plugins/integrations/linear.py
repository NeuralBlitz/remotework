"""
Linear Integration Plugin
Issues, projects, teams, cycles via Linear GraphQL API
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.linear")


class LinearClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("LINEAR_API_KEY", "")
        self.base_url = "https://api.linear.app/graphql"

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }

    def _query(self, query: str, variables: Dict = None) -> Dict:
        import requests
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        resp = requests.post(self.base_url, headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if "errors" in result:
            raise Exception(f"Linear API error: {result['errors']}")
        return result.get("data", {})

    def get_teams(self) -> List[Dict]:
        data = self._query("""
            query { teams { nodes { id name key description } } }
        """)
        return data.get("teams", {}).get("nodes", [])

    def get_issues(self, team_id: str = None, state: str = None, limit: int = 50) -> List[Dict]:
        filters = []
        if team_id:
            filters.append(f'team: {{ id: {{ eq: "{team_id}" }} }}')
        if state:
            filters.append(f'state: {{ name: {{ eq: "{state}" }} }}')
        filter_str = f'filter: {{ {", ".join(filters)} }}' if filters else ""
        data = self._query(f"""
            query {{
                issues(first: {limit}, {filter_str}) {{
                    nodes {{ id identifier title description state {{ name }} priority assignee {{ name }} }}
                }}
            }}
        """)
        return data.get("issues", {}).get("nodes", [])

    def get_issue(self, issue_id: str) -> Dict:
        data = self._query(f"""
            query {{
                issue(id: "{issue_id}") {{
                    id identifier title description
                    state {{ name }}
                    priority
                    assignee {{ name }}
                    labels {{ nodes {{ name }} }}
                    comments {{ nodes {{ body createdAt user {{ name }} }} }}
                }}
            }}
        """)
        return data.get("issue", {})

    def create_issue(self, team_id: str, title: str, description: str = "",
                     priority: int = 0, assignee_id: str = None) -> Dict:
        vars = {"teamId": team_id, "title": title, "description": description, "priority": priority}
        if assignee_id:
            vars["assigneeId"] = assignee_id
        data = self._query("""
            mutation CreateIssue($teamId: String!, $title: String!, $description: String, $priority: Int, $assigneeId: String) {
                issueCreate(input: { teamId: $teamId, title: $title, description: $description, priority: $priority, assigneeId: $assigneeId }) {
                    success issue { id identifier title }
                }
            }
        """, vars)
        return data.get("issueCreate", {})

    def update_issue(self, issue_id: str, title: str = None, state_id: str = None,
                     priority: int = None) -> Dict:
        fields = []
        if title:
            fields.append(f'title: "{title}"')
        if state_id:
            fields.append(f'stateId: "{state_id}"')
        if priority is not None:
            fields.append(f'priority: {priority}')
        data = self._query(f"""
            mutation {{
                issueUpdate(id: "{issue_id}", input: {{ {", ".join(fields)} }}) {{
                    success issue {{ id identifier title }}
                }}
            }}
        """)
        return data.get("issueUpdate", {})

    def add_comment(self, issue_id: str, body: str) -> Dict:
        data = self._query(f"""
            mutation {{
                commentCreate(input: {{ issueId: "{issue_id}", body: "{body}" }}) {{
                    success comment {{ id body }}
                }}
            }}
        """)
        return data.get("commentCreate", {})

    def get_projects(self, team_id: str = None) -> List[Dict]:
        filter_str = f'filter: {{ teams: {{ some: {{ id: {{ eq: "{team_id}" }} }} }} }}' if team_id else ""
        data = self._query(f"""
            query {{
                projects({filter_str}) {{
                    nodes {{ id name description state progress }}
                }}
            }}
        """)
        return data.get("projects", {}).get("nodes", [])

    def search_issues(self, query: str, limit: int = 25) -> List[Dict]:
        data = self._query(f"""
            query {{
                issueSearch(term: "{query}", first: {limit}) {{
                    nodes {{ id identifier title description state {{ name }} }}
                }}
            }}
        """)
        return data.get("issueSearch", {}).get("nodes", [])


def linear_get_issues_cmd(team_id: str = "") -> List[Dict]:
    """Get issues from Linear."""
    client = LinearClient()
    return client.get_issues(team_id=team_id or None)


def linear_create_issue_cmd(team_id: str = "", title: str = "", description: str = "") -> Dict:
    """Create an issue in Linear."""
    client = LinearClient()
    return client.create_issue(team_id, title, description)


def linear_search_cmd(query: str = "") -> List[Dict]:
    """Search issues in Linear."""
    client = LinearClient()
    return client.search_issues(query)


def linear_get_projects_cmd() -> List[Dict]:
    """Get projects from Linear."""
    client = LinearClient()
    return client.get_projects()


def register(plugin):
    plugin.register_command("linear_get_issues", linear_get_issues_cmd)
    plugin.register_command("linear_create_issue", linear_create_issue_cmd)
    plugin.register_command("linear_search", linear_search_cmd)
    plugin.register_command("linear_get_projects", linear_get_projects_cmd)
    plugin.set_resource("client_class", LinearClient)


PLUGIN_METADATA = {
    "name": "linear",
    "version": "1.0.0",
    "description": "Linear integration - Issues, projects, teams via GraphQL API",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["linear", "issues", "projects", "project-management"],
    "dependencies": [],
    "permissions": ["network_access", "read_env"],
    "min_mito_version": "1.0.0",
}


linear_plugin = {
    "metadata": PLUGIN_METADATA,
    "register": register,
}
