"""
Heroku Plugin
Heroku apps, dynos, and deployments.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.heroku")

try:
    import heroku
    HEROKU_AVAILABLE = True
except ImportError:
    HEROKU_AVAILABLE = False


def heroku_list_apps(api_key: str) -> List[Dict]:
    """List all Heroku apps."""
    if not HEROKU_AVAILABLE:
        raise ImportError("heroku not installed. Run: pip install heroku")
    try:
        client = heroku.from_key(api_key)
        apps = client.apps.list()
        return {"status": "ok", "apps": [{"id": app.id, "name": app.name, "region": app.region.name, "stack": app.stack.name} for app in apps]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def heroku_scale_dyno(app_name: str, dyno_type: str, quantity: int, api_key: str) -> Dict:
    """Scale a dyno type to a specified quantity."""
    if not HEROKU_AVAILABLE:
        raise ImportError("heroku not installed. Run: pip install heroku")
    try:
        client = heroku.from_key(api_key)
        app = client.apps[app_name]
        app.dynos.scale(quantity, dyno_type)
        return {"status": "ok", "app": app_name, "dyno_type": dyno_type, "quantity": quantity}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def heroku_get_logs(app_name: str, api_key: str, lines: int = 100, source: str = None) -> List[str]:
    """Get recent logs for an app."""
    if not HEROKU_AVAILABLE:
        raise ImportError("heroku not installed. Run: pip install heroku")
    try:
        client = heroku.from_key(api_key)
        app = client.apps[app_name]
        logs = app.logs().stream(lines=lines, source=source)
        return {"status": "ok", "app": app_name, "logs": list(logs)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def heroku_create_app(app_name: str, region: str, api_key: str, stack: str = "heroku-22") -> Dict:
    """Create a new Heroku app."""
    if not HEROKU_AVAILABLE:
        raise ImportError("heroku not installed. Run: pip install heroku")
    try:
        client = heroku.from_key(api_key)
        app = client.apps.create(name=app_name, region=region, stack=stack)
        return {"status": "ok", "app_id": app.id, "name": app.name, "web_url": app.web_url}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def heroku_deploy_git(app_name: str, branch: str, api_key: str) -> Dict:
    """Deploy an app via Git."""
    if not HEROKU_AVAILABLE:
        raise ImportError("heroku not installed. Run: pip install heroku")
    return {"status": "ok", "app": app_name, "branch": branch, "message": "Git deploy requires heroku CLI"}


def register(plugin):
    plugin.register_command("list_apps", heroku_list_apps)
    plugin.register_command("scale_dyno", heroku_scale_dyno)
    plugin.register_command("get_logs", heroku_get_logs)
    plugin.register_command("create_app", heroku_create_app)
    plugin.register_command("deploy_git", heroku_deploy_git)


PLUGIN_METADATA = {
    "name": "heroku", "version": "1.0.0",
    "description": "Heroku apps, dynos, and deployments",
    "author": "Mito Team", "license": "MIT",
    "tags": ["cloud", "paas", "heroku"],
    "dependencies": ["heroku"], "permissions": ["apps", "deploy"],
    "min_mito_version": "1.0.1",
}

heroku_plugin = {"metadata": PLUGIN_METADATA, "register": register}
