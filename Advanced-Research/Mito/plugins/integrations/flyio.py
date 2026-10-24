"""
Fly.io Plugin
Fly.io apps, machines, and scaling.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.flyio")

try:
    from flyctl import fly
    FLYIO_AVAILABLE = True
except ImportError:
    FLYIO_AVAILABLE = False


def flyio_list_apps(access_token: str) -> List[Dict]:
    """List all Fly.io apps."""
    if not FLYIO_AVAILABLE:
        raise ImportError("flyctl not installed. Run: pip install flyctl")
    try:
        apps = fly.list_apps(token=access_token)
        return {"status": "ok", "apps": [{"id": a["id"], "name": a["name"], "status": a["status"]} for a in apps]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def flyio_launch_app(name: str, org: str, region: str, access_token: str) -> Dict:
    """Launch a new Fly.io app."""
    if not FLYIO_AVAILABLE:
        raise ImportError("flyctl not installed. Run: pip install flyctl")
    try:
        app = fly.launch_app(name=name, org=org, region=region, token=access_token)
        return {"status": "ok", "id": app["id"], "name": app["name"]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def flyio_scale_app(app_name: str, count: int, access_token: str, region: str = None) -> Dict:
    """Scale an app's machine count."""
    if not FLYIO_AVAILABLE:
        raise ImportError("flyctl not installed. Run: pip install flyctl")
    try:
        result = fly.scale_app(app_name=app_name, count=count, region=region, token=access_token)
        return {"status": "ok", "app": app_name, "count": count, "result": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def flyio_get_status(app_name: str, access_token: str) -> Dict:
    """Get status and info about an app."""
    if not FLYIO_AVAILABLE:
        raise ImportError("flyctl not installed. Run: pip install flyctl")
    try:
        status = fly.get_status(app_name=app_name, token=access_token)
        return {"status": "ok", "app": app_name, "status": status}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def register(plugin):
    plugin.register_command("list_apps", flyio_list_apps)
    plugin.register_command("launch_app", flyio_launch_app)
    plugin.register_command("scale_app", flyio_scale_app)
    plugin.register_command("get_status", flyio_get_status)


PLUGIN_METADATA = {
    "name": "flyio", "version": "1.0.0",
    "description": "Fly.io apps, machines, and scaling",
    "author": "Mito Team", "license": "MIT",
    "tags": ["cloud", "infrastructure", "flyio"],
    "dependencies": ["flyctl"], "permissions": ["apps", "compute"],
    "min_mito_version": "1.0.1",
}

flyio_plugin = {"metadata": PLUGIN_METADATA, "register": register}
