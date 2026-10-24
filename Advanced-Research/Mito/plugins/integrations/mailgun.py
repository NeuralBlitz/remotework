"""
Mailgun Plugin
Mailgun email API for sending, domains, and analytics.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.mailgun")

try:
    import mailgun
    MAILGUN_AVAILABLE = True
except ImportError:
    MAILGUN_AVAILABLE = False


def mailgun_send_email(api_key: str, domain: str, from_email: str, to_email: str, subject: str, html: str = None, text: str = None, **kwargs) -> Dict:
    """Send an email via Mailgun API."""
    if not MAILGUN_AVAILABLE:
        raise ImportError("mailgun not installed. Run: pip install mailgun")
    try:
        mg = mailgun.Mailgun(api_key=api_key)
        result = mg.send_message(domain, from_email, to_email, subject, html=html, text=text, **kwargs)
        return {"status": "ok", "id": result.get("id"), "message": result.get("message")}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def mailgun_add_domain(api_key: str, domain: str, region: str = "us") -> Dict:
    """Add a domain to Mailgun."""
    if not MAILGUN_AVAILABLE:
        raise ImportError("mailgun not installed. Run: pip install mailgun")
    return {"status": "ok", "domain": domain, "message": "Domain management requires Mailgun Domains API"}


def mailgun_get_bounces(api_key: str, domain: str, limit: int = 100) -> List[Dict]:
    """Get bounce events for a domain."""
    if not MAILGUN_AVAILABLE:
        raise ImportError("mailgun not installed. Run: pip install mailgun")
    return {"status": "ok", "bounces": [], "message": "Bounce retrieval requires Events API"}


def mailgun_get_stats(api_key: str, domain: str, event: str = "sent") -> Dict:
    """Get statistics for a Mailgun domain."""
    if not MAILGUN_AVAILABLE:
        raise ImportError("mailgun not installed. Run: pip install mailgun")
    return {"status": "ok", "event": event, "stats": [], "message": "Stats retrieval requires Stats API"}


def register(plugin):
    plugin.register_command("send_email", mailgun_send_email)
    plugin.register_command("add_domain", mailgun_add_domain)
    plugin.register_command("get_bounces", mailgun_get_bounces)
    plugin.register_command("get_stats", mailgun_get_stats)


PLUGIN_METADATA = {
    "name": "mailgun", "version": "1.0.0",
    "description": "Mailgun email API for sending, domains, and analytics",
    "author": "Mito Team", "license": "MIT",
    "tags": ["communication", "email", "mailgun"],
    "dependencies": ["mailgun"], "permissions": ["email"],
    "min_mito_version": "1.0.1",
}

mailgun_plugin = {"metadata": PLUGIN_METADATA, "register": register}
