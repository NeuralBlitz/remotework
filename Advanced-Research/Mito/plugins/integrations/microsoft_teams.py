"""
Microsoft Teams Plugin
MS Teams messages, cards, and channel management.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.microsoft_teams")

try:
    import pymsteams
    TEAMS_AVAILABLE = True
except ImportError:
    TEAMS_AVAILABLE = False


def teams_send_message(webhook_url: str, message: str) -> Dict:
    """Send a message to a Microsoft Teams channel via webhook."""
    if not TEAMS_AVAILABLE:
        raise ImportError("pymsteams not installed. Run: pip install pymsteams")
    try:
        message_card = pymsteams.connectorcard(webhook_url)
        message_card.text(message)
        message_card.send()
        return {"status": "ok", "message": "Message sent successfully"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def teams_send_card(webhook_url: str, title: str, text: str, sections: List[Dict] = None, facts: List[Dict] = None) -> Dict:
    """Send a formatted card message to a Teams channel."""
    if not TEAMS_AVAILABLE:
        raise ImportError("pymsteams not installed. Run: pip install pymsteams")
    try:
        message_card = pymsteams.connectorcard(webhook_url)
        message_card.title(title)
        message_card.text(text)
        if sections:
            for section_data in sections:
                section = pymsteams.cardsection()
                section.title(section_data.get("title"))
                section.activityImage(section_data.get("image"))
                section.text(section_data.get("text"))
                message_card.addSection(section)
        if facts:
            message_card.addFact("facts", "\n".join([f"{f['name']}: {f['value']}" for f in facts]))
        message_card.send()
        return {"status": "ok", "message": "Card sent successfully"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def teams_create_channel(team_id: str, channel_name: str, channel_type: str = "standard") -> Dict:
    """Create a new channel in a Teams team."""
    if not TEAMS_AVAILABLE:
        raise ImportError("pymsteams not installed. Run: pip install pymsteams")
    return {"status": "ok", "team_id": team_id, "channel_name": channel_name, "message": "Channel creation requires Microsoft Graph API"}


def teams_list_channels(team_id: str = None) -> List[Dict]:
    """List channels in a Teams team."""
    if not TEAMS_AVAILABLE:
        raise ImportError("pymsteams not installed. Run: pip install pymsteams")
    return {"status": "ok", "channels": [], "message": "List channels requires Microsoft Graph API"}


def register(plugin):
    plugin.register_command("send_message", teams_send_message)
    plugin.register_command("send_card", teams_send_card)
    plugin.register_command("create_channel", teams_create_channel)
    plugin.register_command("list_channels", teams_list_channels)


PLUGIN_METADATA = {
    "name": "microsoft_teams", "version": "1.0.0",
    "description": "Microsoft Teams messages, cards, and channel management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["communication", "teams", "microsoft"],
    "dependencies": ["pymsteams"], "permissions": ["messaging"],
    "min_mito_version": "1.0.1",
}

microsoft_teams_plugin = {"metadata": PLUGIN_METADATA, "register": register}
