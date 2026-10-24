"""
Discord Plugin
Discord webhooks, embeds, and bot commands.
"""
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("mito.plugins.discord")

try:
    import discord
    from discord import Embed, Color
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False


def discord_send_message(webhook_url: str, content: str, username: str = None) -> Dict:
    """Send a message to a Discord channel via webhook."""
    if not DISCORD_AVAILABLE:
        raise ImportError("discord.py not installed. Run: pip install discord.py")
    import requests
    payload = {"content": content}
    if username:
        payload["username"] = username
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code in [200, 204]:
            return {"status": "ok", "message": "Message sent successfully"}
        return {"status": "error", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def discord_send_embed(webhook_url: str, title: str, description: str, color: int = 0x3498db, fields: List[Dict] = None, footer: str = None) -> Dict:
    """Send a rich embed message to a Discord channel."""
    if not DISCORD_AVAILABLE:
        raise ImportError("discord.py not installed. Run: pip install discord.py")
    import requests
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "fields": fields or [],
    }
    if footer:
        embed["footer"] = {"text": footer}
    payload = {"embeds": [embed]}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code in [200, 204]:
            return {"status": "ok", "message": "Embed sent successfully"}
        return {"status": "error", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def discord_get_channel(bot_token: str, channel_id: int) -> Dict:
    """Get information about a Discord channel."""
    if not DISCORD_AVAILABLE:
        raise ImportError("discord.py not installed. Run: pip install discord.py")
    return {"status": "ok", "channel_id": channel_id, "message": "Bot functionality requires async client"}


def discord_list_channels(guild_id: int, bot_token: str = None) -> List[Dict]:
    """List all channels in a Discord guild."""
    if not DISCORD_AVAILABLE:
        raise ImportError("discord.py not installed. Run: pip install discord.py")
    return {"status": "ok", "channels": [], "message": "List channels requires bot with intents"}


def register(plugin):
    plugin.register_command("send_message", discord_send_message)
    plugin.register_command("send_embed", discord_send_embed)
    plugin.register_command("get_channel", discord_get_channel)
    plugin.register_command("list_channels", discord_list_channels)


PLUGIN_METADATA = {
    "name": "discord", "version": "1.0.0",
    "description": "Discord webhooks, embeds, and bot commands",
    "author": "Mito Team", "license": "MIT",
    "tags": ["communication", "discord", "webhooks"],
    "dependencies": ["discord.py"], "permissions": ["messaging"],
    "min_mito_version": "1.0.1",
}

discord_plugin = {"metadata": PLUGIN_METADATA, "register": register}


class DiscordClient:
    def __init__(self, base_url: str = "https://discord.com/api"):
        self.base_url = base_url

    def create_embed(self, title: str, description: str, color: int = 0x3498db):
        return {"title": title, "description": description, "color": color}
