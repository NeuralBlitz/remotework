"""
Twilio Plugin
Twilio SMS, WhatsApp, and voice capabilities.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.twilio")

try:
    from twilio.rest import Client
    from twilio.base.exceptions import TwilioRestException
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False


def twilio_send_sms(account_sid: str, auth_token: str, from_number: str, to_number: str, body: str) -> Dict:
    """Send an SMS message via Twilio."""
    if not TWILIO_AVAILABLE:
        raise ImportError("twilio not installed. Run: pip install twilio")
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(body=body, from_=from_number, to=to_number)
        return {"status": "ok", "sid": message.sid, "status": message.status, "to": to_number}
    except TwilioRestException as e:
        return {"status": "error", "error": str(e)}


def twilio_send_whatsapp(account_sid: str, auth_token: str, from_number: str, to_number: str, body: str) -> Dict:
    """Send a WhatsApp message via Twilio."""
    if not TWILIO_AVAILABLE:
        raise ImportError("twilio not installed. Run: pip install twilio")
    try:
        client = Client(account_sid, auth_token)
        from_whatsapp = f"whatsapp:{from_number}"
        to_whatsapp = f"whatsapp:{to_number}"
        message = client.messages.create(body=body, from_=from_whatsapp, to=to_whatsapp)
        return {"status": "ok", "sid": message.sid, "status": message.status}
    except TwilioRestException as e:
        return {"status": "error", "error": str(e)}


def twilio_make_call(account_sid: str, auth_token: str, from_number: str, to_number: str, twiml_url: str = None, twiml: str = None) -> Dict:
    """Make a voice call via Twilio."""
    if not TWILIO_AVAILABLE:
        raise ImportError("twilio not installed. Run: pip install twilio")
    try:
        client = Client(account_sid, auth_token)
        call = client.calls.create(to=to_number, from_=from_number, twiml_url=twiml_url, twiml=twiml)
        return {"status": "ok", "sid": call.sid, "status": call.status}
    except TwilioRestException as e:
        return {"status": "error", "error": str(e)}


def twilio_get_messages(account_sid: str, auth_token: str, to_number: str = None, from_number: str = None, limit: int = 50) -> List[Dict]:
    """Get SMS messages."""
    if not TWILIO_AVAILABLE:
        raise ImportError("twilio not installed. Run: pip install twilio")
    try:
        client = Client(account_sid, auth_token)
        filters = {"to": to_number, "from_": from_number}
        filters = {k: v for k, v in filters.items() if v}
        messages = client.messages.list(**filters, limit=limit)
        return {"status": "ok", "messages": [{"sid": m.sid, "to": m.to, "from": m.from_, "body": m.body, "status": m.status} for m in messages]}
    except TwilioRestException as e:
        return {"status": "error", "error": str(e)}


def register(plugin):
    plugin.register_command("send_sms", twilio_send_sms)
    plugin.register_command("send_whatsapp", twilio_send_whatsapp)
    plugin.register_command("make_call", twilio_make_call)
    plugin.register_command("get_messages", twilio_get_messages)


PLUGIN_METADATA = {
    "name": "twilio", "version": "1.0.0",
    "description": "Twilio SMS, WhatsApp, and voice capabilities",
    "author": "Mito Team", "license": "MIT",
    "tags": ["communication", "sms", "twilio"],
    "dependencies": ["twilio"], "permissions": ["messaging", "voice"],
    "min_mito_version": "1.0.1",
}

twilio_plugin = {"metadata": PLUGIN_METADATA, "register": register}


class TwilioClient:
    def __init__(self, account_sid: str = "", auth_token: str = "", base_url: str = "https://api.twilio.com"):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.base_url = base_url

    def _headers(self):
        return {}
