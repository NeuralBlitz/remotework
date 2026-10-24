"""
Git Operations Plugin
Clone, commit, push, pull, branch, diff, log, status.
"""

import os
import subprocess
import logging
from typing import Dict, List, Optional

logger = logging.getLogger("mito.plugins.git_ops")


class GitOpsClient:
    def __init__(self, repo_path: str = "."):
        self.repo_path = os.path.expanduser(repo_path)

    def _run(self, *args, check: bool = True) -> Dict[str, str]:
        try:
            result = subprocess.run(
                ["git"] + list(args),
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if check and result.returncode != 0:
                raise RuntimeError(result.stderr.strip())
            return {"stdout": result.stdout.strip(), "stderr": result.stderr.strip(), "code": result.returncode}
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out", "stdout": "", "stderr": "", "code": -1}
        except FileNotFoundError:
            return {"error": "git not found", "stdout": "", "stderr": "", "code": -1}

    def status(self) -> Dict:
        return self._run("status", "--porcelain")

    def log(self, max_count: int = 10, oneline: bool = True) -> List[str]:
        flag = "--oneline" if oneline else "-10"
        result = self._run("log", f"-{max_count}", "--format=%H|%an|%ae|%at|%s")
        if result.get("error"):
            return [result.get("error", "")]
        commits = []
        for line in result["stdout"].splitlines():
            parts = line.split("|", 4)
            if len(parts) >= 5:
                commits.append({
                    "hash": parts[0],
                    "author": parts[1],
                    "email": parts[2],
                    "timestamp": int(parts[3]),
                    "message": parts[4],
                })
        return commits

    def diff(self, ref1: str = "", ref2: str = "", cached: bool = False) -> str:
        if cached:
            return self._run("diff", "--cached", ref1)["stdout"]
        if ref1 and ref2:
            return self._run("diff", ref1, ref2)["stdout"]
        elif ref1:
            return self._run("diff", ref1)["stdout"]
        return self._run("diff")["stdout"]

    def branch_list(self) -> List[Dict]:
        result = self._run("branch", "-a", "--format=%(HEAD)|%(refname:short)|%(upstream:short)|%(objectname:short)")
        branches = []
        for line in result["stdout"].splitlines():
            parts = line.split("|")
            if len(parts) >= 3:
                branches.append({
                    "current": parts[0].strip() == "*",
                    "name": parts[1].strip(),
                    "upstream": parts[2].strip(),
                    "hash": parts[3].strip() if len(parts) > 3 else "",
                })
        return branches

    def current_branch(self) -> str:
        return self._run("branch", "--show-current")["stdout"]

    def add(self, paths: str = ".") -> Dict:
        return self._run("add", paths)

    def commit(self, message: str, amend: bool = False) -> Dict:
        args = ["commit", "-m", message]
        if amend:
            args.insert(2, "--amend")
        return self._run(*args)

    def push(self, remote: str = "origin", branch: str = "", force: bool = False) -> Dict:
        args = ["push"]
        if force:
            args.append("--force")
        args.append(remote)
        if branch:
            args.append(branch)
        return self._run(*args)

    def pull(self, remote: str = "origin", branch: str = "") -> Dict:
        args = ["pull"]
        if remote:
            args.append(remote)
        if branch:
            args.append(branch)
        return self._run(*args)

    def clone(self, url: str, target_dir: str = ".") -> Dict:
        try:
            result = subprocess.run(
                ["git", "clone", url, target_dir],
                capture_output=True,
                text=True,
                timeout=120,
            )
            return {"stdout": result.stdout.strip(), "stderr": result.stderr.strip(), "code": result.returncode}
        except Exception as e:
            return {"error": str(e), "stdout": "", "stderr": "", "code": -1}

    def checkout(self, ref: str, create_branch: bool = False, branch_name: str = "") -> Dict:
        args = ["checkout"]
        if create_branch:
            args.extend(["-b", branch_name or ref])
        else:
            args.append(ref)
        return self._run(*args)

    def stash(self, action: str = "push", message: str = "") -> Dict:
        args = ["stash"]
        if action == "push":
            args.append("push")
            if message:
                args.extend(["-m", message])
        elif action == "pop":
            args.append("pop")
        elif action == "list":
            args.append("list")
        elif action == "drop":
            args.append("drop")
        return self._run(*args)

    def remote_list(self) -> List[Dict]:
        result = self._run("remote", "-v")
        remotes = []
        for line in result["stdout"].splitlines():
            parts = line.split()
            if len(parts) >= 2:
                remotes.append({"name": parts[0], "url": parts[1]})
        return remotes

    def remote_add(self, name: str, url: str) -> Dict:
        return self._run("remote", "add", name, url)


def git_status_cmd(repo: str = ".") -> Dict:
    """Get git status in porcelain format."""
    return GitOpsClient(repo).status()


def git_log_cmd(repo: str = ".", max_count: int = 10) -> List[Dict]:
    """Get recent commit history."""
    return GitOpsClient(repo).log(max_count=max_count)


def git_diff_cmd(repo: str = ".", ref1: str = "", ref2: str = "", cached: bool = False) -> str:
    """Get diff between refs or working tree."""
    return GitOpsClient(repo).diff(ref1, ref2, cached=cached)


def git_branch_cmd(repo: str = ".") -> List[Dict]:
    """List all branches."""
    return GitOpsClient(repo).branch_list()


def git_commit_cmd(repo: str = ".", message: str = "", amend: bool = False) -> Dict:
    """Create a commit with a message."""
    return GitOpsClient(repo).commit(message, amend=amend)


def git_push_cmd(repo: str = ".", remote: str = "origin", force: bool = False) -> Dict:
    """Push to remote."""
    return GitOpsClient(repo).push(remote=remote, force=force)


def git_pull_cmd(repo: str = ".", remote: str = "origin") -> Dict:
    """Pull from remote."""
    return GitOpsClient(repo).pull(remote=remote)


def git_add_cmd(repo: str = ".", paths: str = ".") -> Dict:
    """Stage files for commit."""
    return GitOpsClient(repo).add(paths)


def git_stash_cmd(repo: str = ".", action: str = "push") -> Dict:
    """Stash changes (push, pop, list, drop)."""
    return GitOpsClient(repo).stash(action=action)


def register(plugin):
    plugin.register_command("git_status", git_status_cmd)
    plugin.register_command("git_log", git_log_cmd)
    plugin.register_command("git_diff", git_diff_cmd)
    plugin.register_command("git_branch", git_branch_cmd)
    plugin.register_command("git_commit", git_commit_cmd)
    plugin.register_command("git_push", git_push_cmd)
    plugin.register_command("git_pull", git_pull_cmd)
    plugin.register_command("git_add", git_add_cmd)
    plugin.register_command("git_stash", git_stash_cmd)
    plugin.set_resource("client_class", GitOpsClient)


PLUGIN_METADATA = {
    "name": "git_ops",
    "version": "1.0.0",
    "description": "Git operations - status, log, diff, branch, commit, push, pull, stash",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["git", "version-control", "commit", "push", "pull"],
    "dependencies": [],
    "permissions": ["execute_commands", "read_files", "write_files"],
    "min_mito_version": "1.0.1",
}


git_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
