"""
Slack Plugin
Slack messaging, channels, reactions, and threads integration.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.slack")

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False


def slack_send_message(channel: str, text: str, thread_ts: str = None) -> Dict:
    """Send a message to a Slack channel."""
    if not SLACK_AVAILABLE:
        raise ImportError("slack-sdk not installed. Run: pip install slack-sdk")
    client = WebClient()
    try:
        response = client.chat_postMessage(channel=channel, text=text, thread_ts=thread_ts)
        return {"status": "ok", "ts": response["ts"], "channel": channel}
    except SlackApiError as e:
        return {"status": "error", "error": str(e)}


def slack_list_channels(limit: int = 100) -> List[Dict]:
    """List all Slack channels."""
    if not SLACK_AVAILABLE:
        raise ImportError("slack-sdk not installed. Run: pip install slack-sdk")
    client = WebClient()
    try:
        response = client.conversations_list(limit=limit, types="public_channel,private_channel")
        channels = [{"id": c["id"], "name": c["name"], "is_private": c.get("is_private", False)} for c in response["channels"]]
        return {"status": "ok", "channels": channels}
    except SlackApiError as e:
        return {"status": "error", "error": str(e)}


def slack_post_file(channel: str, file_path: str, title: str = None, initial_comment: str = None) -> Dict:
    """Upload and post a file to a Slack channel."""
    if not SLACK_AVAILABLE:
        raise ImportError("slack-sdk not installed. Run: pip install slack-sdk")
    client = WebClient()
    try:
        response = client.files_upload(channel=channel, file=file_path, title=title, initial_comment=initial_comment)
        return {"status": "ok", "file_id": response["file"]["id"], "permalink": response["file"]["permalink"]}
    except SlackApiError as e:
        return {"status": "error", "error": str(e)}


def slack_set_status(status_text: str, status_emoji: str, status_expiration: int = None) -> Dict:
    """Set the authenticated user's Slack status."""
    if not SLACK_AVAILABLE:
        raise ImportError("slack-sdk not installed. Run: pip install slack-sdk")
    client = WebClient()
    try:
        profile = {"status_text": status_text, "status_emoji": status_emoji}
        if status_expiration:
            profile["status_expiration"] = status_expiration
        response = client.users_profile_set(profile=profile)
        return {"status": "ok", "profile": response["profile"]}
    except SlackApiError as e:
        return {"status": "error", "error": str(e)}


def slack_search_messages(query: str, count: int = 20, sort: str = "score") -> List[Dict]:
    """Search for messages matching a query."""
    if not SLACK_AVAILABLE:
        raise ImportError("slack-sdk not installed. Run: pip install slack-sdk")
    client = WebClient()
    try:
        response = client.search_messages(query=query, count=count, sort=sort)
        messages = [{"text": m["text"], "user": m["user"], "ts": m["ts"], "channel": m["channel"]["id"]} for m in response["messages"]["matches"]]
        return {"status": "ok", "matches": messages, "total": response["messages"]["total"]}
    except SlackApiError as e:
        return {"status": "error", "error": str(e)}


def register(plugin):
    plugin.register_command("send_message", slack_send_message)
    plugin.register_command("list_channels", slack_list_channels)
    plugin.register_command("post_file", slack_post_file)
    plugin.register_command("set_status", slack_set_status)
    plugin.register_command("search_messages", slack_search_messages)


PLUGIN_METADATA = {
    "name": "slack", "version": "1.0.0",
    "description": "Slack messaging, channels, reactions, and threads integration",
    "author": "Mito Team", "license": "MIT",
    "tags": ["communication", "messaging", "slack"],
    "dependencies": ["slack-sdk"], "permissions": ["messaging", "files"],
    "min_mito_version": "1.0.1",
}

slack_plugin = {"metadata": PLUGIN_METADATA, "register": register}


class SlackClient:
    def __init__(self, token: str = "", base_url: str = "https://slack.com/api"):
        self.token = token
        self.base_url = base_url

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}
