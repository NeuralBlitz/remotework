"""
Netlify Plugin
Netlify sites, deploys, and build management.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.netlify")

try:
    import netlify
    NETLIFY_AVAILABLE = True
except ImportError:
    NETLIFY_AVAILABLE = False


def netlify_list_sites(access_token: str) -> List[Dict]:
    """List all Netlify sites."""
    if not NETLIFY_AVAILABLE:
        raise ImportError("netlify not installed. Run: pip install netlify")
    try:
        api = netlify.Netlify(access_token)
        sites = api.list_sites()
        return {"status": "ok", "sites": [{"id": s["id"], "name": s["name"], "url": s["url"], "ssl_url": s.get("ssl_url")} for s in sites]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def netlify_create_site(name: str, access_token: str, custom_domain: str = None) -> Dict:
    """Create a new Netlify site."""
    if not NETLIFY_AVAILABLE:
        raise ImportError("netlify not installed. Run: pip install netlify")
    try:
        api = netlify.Netlify(access_token)
        site = api.create_site(name=name, custom_domain=custom_domain)
        return {"status": "ok", "id": site["id"], "name": site["name"], "url": site["url"]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def netlify_deploy_site(site_id: str, access_token: str, files: Dict, draft: bool = False) -> Dict:
    """Deploy files to a Netlify site."""
    if not NETLIFY_AVAILABLE:
        raise ImportError("netlify not installed. Run: pip install netlify")
    try:
        api = netlify.Netlify(access_token)
        deploy = api.deploy_site(site_id, files=files, draft=draft)
        return {"status": "ok", "deploy_id": deploy["id"], "url": deploy["deploy_url"]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def netlify_get_builds(site_id: str, access_token: str) -> List[Dict]:
    """Get build history for a site."""
    if not NETLIFY_AVAILABLE:
        raise ImportError("netlify not installed. Run: pip install netlify")
    return {"status": "ok", "site_id": site_id, "builds": [], "message": "Build history requires Build API"}


def register(plugin):
    plugin.register_command("list_sites", netlify_list_sites)
    plugin.register_command("create_site", netlify_create_site)
    plugin.register_command("deploy_site", netlify_deploy_site)
    plugin.register_command("get_builds", netlify_get_builds)


PLUGIN_METADATA = {
    "name": "netlify", "version": "1.0.0",
    "description": "Netlify sites, deploys, and build management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["cloud", "deployment", "netlify"],
    "dependencies": ["netlify"], "permissions": ["sites", "deploys"],
    "min_mito_version": "1.0.1",
}

netlify_plugin = {"metadata": PLUGIN_METADATA, "register": register}
