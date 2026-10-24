"""
Vercel Plugin
Vercel deployments and project management.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.vercel")

try:
    import vercel
    VERCEL_AVAILABLE = True
except ImportError:
    VERCEL_AVAILABLE = False


def vercel_list_deployments(team_id: str = None, limit: int = 20) -> List[Dict]:
    """List deployments in Vercel."""
    if not VERCEL_AVAILABLE:
        raise ImportError("vercel not installed. Run: pip install vercel")
    try:
        client = vercel.Client()
        deployments = client.deployments.list(teamId=team_id, limit=limit)
        return {"status": "ok", "deployments": [{"uid": d["uid"], "name": d["name"], "state": d["state"], "url": d["url"]} for d in deployments["deployments"]]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def vercel_create_deployment(name: str, files: List[Dict], project_settings: Dict = None, team_id: str = None) -> Dict:
    """Create a new deployment."""
    if not VERCEL_AVAILABLE:
        raise ImportError("vercel not installed. Run: pip install vercel")
    try:
        client = vercel.Client()
        deployment = client.deployments.create(name=name, files=files, projectSettings=project_settings, teamId=team_id)
        return {"status": "ok", "url": deployment["url"], "id": deployment["id"]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def vercel_get_project(name: str, team_id: str = None) -> Dict:
    """Get project details."""
    if not VERCEL_AVAILABLE:
        raise ImportError("vercel not installed. Run: pip install vercel")
    try:
        client = vercel.Client()
        project = client.projects.get(name=name, teamId=team_id)
        return {"status": "ok", "project": project}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def vercel_alias_deployment(deployment_id: str, alias: str, team_id: str = None) -> Dict:
    """Alias a deployment to a URL."""
    if not VERCEL_AVAILABLE:
        raise ImportError("vercel not installed. Run: pip install vercel")
    try:
        client = vercel.Client()
        result = client.alias.create(deploymentId=deployment_id, alias=alias, teamId=team_id)
        return {"status": "ok", "alias": alias, "deployment_id": deployment_id}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def register(plugin):
    plugin.register_command("list_deployments", vercel_list_deployments)
    plugin.register_command("create_deployment", vercel_create_deployment)
    plugin.register_command("get_project", vercel_get_project)
    plugin.register_command("alias_deployment", vercel_alias_deployment)


PLUGIN_METADATA = {
    "name": "vercel", "version": "1.0.0",
    "description": "Vercel deployments and project management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["cloud", "deployment", "vercel"],
    "dependencies": ["vercel"], "permissions": ["deployments"],
    "min_mito_version": "1.0.1",
}

vercel_plugin = {"metadata": PLUGIN_METADATA, "register": register}
