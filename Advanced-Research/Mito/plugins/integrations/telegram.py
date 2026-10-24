"""
Telegram Plugin
Telegram bot API for messaging, media, and updates.
"""
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("mito.plugins.telegram")

try:
    from telegram import Bot, InputMediaPhoto, Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False


def telegram_send_message(bot_token: str, chat_id: int, text: str, parse_mode: str = "Markdown") -> Dict:
    """Send a message to a Telegram chat."""
    if not TELEGRAM_AVAILABLE:
        raise ImportError("python-telegram-bot not installed. Run: pip install python-telegram-bot")
    import asyncio
    
    async def _send():
        bot = Bot(token=bot_token)
        return await bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
    
    try:
        message = asyncio.run(_send())
        return {"status": "ok", "message_id": message.message_id, "chat_id": chat_id}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def telegram_send_photo(bot_token: str, chat_id: int, photo_url: str, caption: str = None) -> Dict:
    """Send a photo to a Telegram chat."""
    if not TELEGRAM_AVAILABLE:
        raise ImportError("python-telegram-bot not installed. Run: pip install python-telegram-bot")
    import asyncio
    
    async def _send():
        bot = Bot(token=bot_token)
        return await bot.send_photo(chat_id=chat_id, photo=photo_url, caption=caption)
    
    try:
        message = asyncio.run(_send())
        return {"status": "ok", "message_id": message.message_id, "photo_id": message.photo[-1].file_id if message.photo else None}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def telegram_get_updates(bot_token: str, limit: int = 100, offset: int = None) -> List[Dict]:
    """Get updates from a Telegram bot."""
    if not TELEGRAM_AVAILABLE:
        raise ImportError("python-telegram-bot not installed. Run: pip install python-telegram-bot")
    import asyncio
    
    async def _get():
        bot = Bot(token=bot_token)
        return await bot.get_updates(offset=offset, limit=limit)
    
    try:
        updates = asyncio.run(_get())
        return {"status": "ok", "updates": [{"id": u.update_id, "message": str(u.message) if u.message else None} for u in updates]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def telegram_set_webhook(bot_token: str, webhook_url: str, secret_token: str = None) -> Dict:
    """Set a webhook URL for a Telegram bot."""
    if not TELEGRAM_AVAILABLE:
        raise ImportError("python-telegram-bot not installed. Run: pip install python-telegram-bot")
    import asyncio
    
    async def _set():
        bot = Bot(token=bot_token)
        return await bot.set_webhook(url=webhook_url, secret_token=secret_token)
    
    try:
        result = asyncio.run(_set())
        return {"status": "ok", "webhook_set": result, "url": webhook_url}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def register(plugin):
    plugin.register_command("send_message", telegram_send_message)
    plugin.register_command("send_photo", telegram_send_photo)
    plugin.register_command("get_updates", telegram_get_updates)
    plugin.register_command("set_webhook", telegram_set_webhook)


PLUGIN_METADATA = {
    "name": "telegram", "version": "1.0.0",
    "description": "Telegram bot API for messaging, media, and updates",
    "author": "Mito Team", "license": "MIT",
    "tags": ["communication", "telegram", "bot"],
    "dependencies": ["python-telegram-bot"], "permissions": ["messaging"],
    "min_mito_version": "1.0.1",
}

telegram_plugin = {"metadata": PLUGIN_METADATA, "register": register}


class TelegramClient:
    def __init__(self, token: str = "", base_url: str = "https://api.telegram.org"):
        self.token = token
        self.base_url = base_url

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}
