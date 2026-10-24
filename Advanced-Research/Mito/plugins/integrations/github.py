"""
GitHub Integration Plugin
Issues, PRs, repos, code search via GitHub REST API
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.github")


class GitHubClient:
    def __init__(self, token: Optional[str] = None, base_url: str = "https://api.github.com"):
        self.token = token or os.environ.get("GITHUB_TOKEN", "")
        self.base_url = base_url

    def _headers(self) -> Dict[str, str]:
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def _request(self, method: str, path: str, data: Dict = None, params: Dict = None) -> Any:
        import requests
        url = f"{self.base_url}{path}"
        resp = requests.request(method, url, headers=self._headers(), json=data, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_repo(self, owner: str, repo: str) -> Dict:
        return self._request("GET", f"/repos/{owner}/{repo}")

    def list_repos(self, org: str = None, user: str = None, per_page: int = 30) -> List[Dict]:
        if org:
            return self._request("GET", f"/orgs/{org}/repos", params={"per_page": per_page})
        elif user:
            return self._request("GET", f"/users/{user}/repos", params={"per_page": per_page})
        return self._request("GET", "/user/repos", params={"per_page": per_page})

    def create_issue(self, owner: str, repo: str, title: str, body: str = "",
                     labels: List[str] = None, assignees: List[str] = None) -> Dict:
        payload = {"title": title, "body": body}
        if labels:
            payload["labels"] = labels
        if assignees:
            payload["assignees"] = assignees
        return self._request("POST", f"/repos/{owner}/{repo}/issues", data=payload)

    def list_issues(self, owner: str, repo: str, state: str = "open",
                    labels: str = None, per_page: int = 30) -> List[Dict]:
        params = {"state": state, "per_page": per_page}
        if labels:
            params["labels"] = labels
        return self._request("GET", f"/repos/{owner}/{repo}/issues", params=params)

    def get_issue(self, owner: str, repo: str, number: int) -> Dict:
        return self._request("GET", f"/repos/{owner}/{repo}/issues/{number}")

    def close_issue(self, owner: str, repo: str, number: int) -> Dict:
        return self._request("PATCH", f"/repos/{owner}/{repo}/issues/{number}", data={"state": "closed"})

    def create_pr(self, owner: str, repo: str, title: str, head: str, base: str = "main",
                  body: str = "", draft: bool = False) -> Dict:
        payload = {"title": title, "head": head, "base": base, "body": body, "draft": draft}
        return self._request("POST", f"/repos/{owner}/{repo}/pulls", data=payload)

    def list_prs(self, owner: str, repo: str, state: str = "open", per_page: int = 30) -> List[Dict]:
        return self._request("GET", f"/repos/{owner}/{repo}/pulls",
                              params={"state": state, "per_page": per_page})

    def get_pr(self, owner: str, repo: str, number: int) -> Dict:
        return self._request("GET", f"/repos/{owner}/{repo}/pulls/{number}")

    def merge_pr(self, owner: str, repo: str, number: int, commit_message: str = "") -> Dict:
        payload = {}
        if commit_message:
            payload["commit_message"] = commit_message
        return self._request("PUT", f"/repos/{owner}/{repo}/pulls/{number}/merge", data=payload)

    def search_code(self, query: str, per_page: int = 30) -> List[Dict]:
        results = self._request("GET", "/search/code", params={"q": query, "per_page": per_page})
        return results.get("items", [])

    def search_repos(self, query: str, per_page: int = 30) -> List[Dict]:
        results = self._request("GET", "/search/repositories", params={"q": query, "per_page": per_page})
        return results.get("items", [])

    def list_commits(self, owner: str, repo: str, sha: str = None, per_page: int = 30) -> List[Dict]:
        params = {"per_page": per_page}
        if sha:
            params["sha"] = sha
        return self._request("GET", f"/repos/{owner}/{repo}/commits", params=params)

    def create_webhook(self, owner: str, repo: str, url: str, events: List[str] = None,
                       secret: str = None) -> Dict:
        config = {"url": url, "content_type": "json"}
        if secret:
            config["secret"] = secret
        payload = {
            "name": "web",
            "active": True,
            "events": events or ["push", "issues", "pull_request"],
            "config": config,
        }
        return self._request("POST", f"/repos/{owner}/{repo}/hooks", data=payload)

    def get_file(self, owner: str, repo: str, path: str, ref: str = None) -> Dict:
        params = {}
        if ref:
            params["ref"] = ref
        return self._request("GET", f"/repos/{owner}/{repo}/contents/{path}", params=params)


# CLI command wrappers
def github_list_issues_cmd(owner: str = "", repo: str = "", state: str = "open") -> List[Dict]:
    """List issues for a GitHub repository."""
    client = GitHubClient()
    return client.list_issues(owner, repo, state=state)


def github_create_issue_cmd(owner: str = "", repo: str = "", title: str = "", body: str = "") -> Dict:
    """Create a GitHub issue."""
    client = GitHubClient()
    return client.create_issue(owner, repo, title, body)


def github_list_prs_cmd(owner: str = "", repo: str = "", state: str = "open") -> List[Dict]:
    """List pull requests for a GitHub repository."""
    client = GitHubClient()
    return client.list_prs(owner, repo, state=state)


def github_search_code_cmd(query: str = "") -> List[Dict]:
    """Search code across GitHub."""
    client = GitHubClient()
    return client.search_code(query)


def github_search_repos_cmd(query: str = "") -> List[Dict]:
    """Search repositories on GitHub."""
    client = GitHubClient()
    return client.search_repos(query)


def register(plugin):
    plugin.register_command("github_list_issues", github_list_issues_cmd)
    plugin.register_command("github_create_issue", github_create_issue_cmd)
    plugin.register_command("github_list_prs", github_list_prs_cmd)
    plugin.register_command("github_search_code", github_search_code_cmd)
    plugin.register_command("github_search_repos", github_search_repos_cmd)
    plugin.set_resource("client_class", GitHubClient)


PLUGIN_METADATA = {
    "name": "github",
    "version": "1.0.0",
    "description": "GitHub integration - Issues, PRs, repos, code search",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["github", "git", "issues", "prs", "code"],
    "dependencies": [],
    "permissions": ["network_access", "read_env"],
    "min_mito_version": "1.0.0",
}


github_plugin = {
    "metadata": PLUGIN_METADATA,
    "register": register,
}
