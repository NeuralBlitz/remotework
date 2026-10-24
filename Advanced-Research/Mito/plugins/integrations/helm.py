"""
Helm Plugin
Kubernetes package management with Helm.
"""
import subprocess
import logging
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.helm")


def helm_install_cmd(name: str = "", chart: str = "", namespace: str = "default", values: str = "") -> Dict:
    args = ["helm", "install", name, chart]
    if namespace:
        args.extend(["--namespace", namespace])
    if values:
        args.extend(["--set", values])
    result = subprocess.run(args, capture_output=True, text=True, timeout=300)
    return {"returncode": result.returncode, "stdout": result.stdout[-2000:], "stderr": result.stderr[-500:]}


def helm_upgrade_cmd(name: str = "", chart: str = "", namespace: str = "default", values: str = "", install: bool = True) -> Dict:
    args = ["helm", "upgrade", name, chart]
    if install:
        args.append("--install")
    if namespace:
        args.extend(["--namespace", namespace])
    if values:
        args.extend(["--set", values])
    result = subprocess.run(args, capture_output=True, text=True, timeout=300)
    return {"returncode": result.returncode, "stdout": result.stdout[-2000:]}


def helm_list_releases_cmd(namespace: str = "default") -> Dict:
    result = subprocess.run(["helm", "list", "--namespace", namespace, "-o", "json"], capture_output=True, text=True, timeout=30)
    import json
    try:
        releases = json.loads(result.stdout)
        return {"releases": releases, "count": len(releases)}
    except Exception:
        return {"raw": result.stdout}


def helm_uninstall_cmd(name: str = "", namespace: str = "default") -> Dict:
    result = subprocess.run(["helm", "uninstall", name, "--namespace", namespace], capture_output=True, text=True, timeout=60)
    return {"returncode": result.returncode, "name": name}


def helm_template_cmd(name: str = "", chart: str = "", values: str = "", namespace: str = "default") -> str:
    args = ["helm", "template", name, chart]
    if values:
        args.extend(["--set", values])
    result = subprocess.run(args, capture_output=True, text=True, timeout=60)
    return {"manifest": result.stdout[-5000:]}


def helm_repo_update_cmd() -> Dict:
    result = subprocess.run(["helm", "repo", "update"], capture_output=True, text=True, timeout=120)
    return {"returncode": result.returncode, "stdout": result.stdout}


def helm_search_cmd(query: str = "") -> Dict:
    result = subprocess.run(["helm", "search", "hub", query], capture_output=True, text=True, timeout=30)
    return {"results": result.stdout[-3000:]}


def register(plugin):
    plugin.register_command("install", helm_install_cmd)
    plugin.register_command("upgrade", helm_upgrade_cmd)
    plugin.register_command("list_releases", helm_list_releases_cmd)
    plugin.register_command("uninstall", helm_uninstall_cmd)
    plugin.register_command("template", helm_template_cmd)
    plugin.register_command("repo_update", helm_repo_update_cmd)
    plugin.register_command("search", helm_search_cmd)


PLUGIN_METADATA = {
    "name": "helm", "version": "1.0.0",
    "description": "Helm Kubernetes package management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["helm", "kubernetes", "charts", "devops"],
    "dependencies": ["helm"], "permissions": ["shell_access"],
    "min_mito_version": "1.0.1",
}

helm_plugin = {"metadata": PLUGIN_METADATA, "register": register}
