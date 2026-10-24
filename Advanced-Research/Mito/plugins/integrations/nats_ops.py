"""
NATS Operations Plugin
Publish and subscribe via NATS.io messaging.
"""
import logging
import json
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.nats_ops")

try:
    import asyncio
    from nats import NATS
    NATS_AVAILABLE = True
except ImportError:
    NATS_AVAILABLE = False


def nats_publish_cmd(subject: str = "", message: str = "", host: str = "localhost", port: int = 4222) -> Dict:
    if not NATS_AVAILABLE:
        raise ImportError("nats-py not installed. Run: pip install nats-py")
    async def _pub():
        nc = NATS()
        await nc.connect(f"nats://{host}:{port}")
        await nc.publish(subject, message.encode())
        await nc.flush()
        await nc.close()
    asyncio.run(_pub())
    return {"subject": subject, "message": message[:100], "status": "published"}


def nats_subscribe_cmd(subject: str = "", host: str = "localhost", port: int = 4222,
                        max_messages: int = 10) -> Dict:
    if not NATS_AVAILABLE:
        raise ImportError("nats-py not installed. Run: pip install nats-py")
    messages = []
    async def _sub():
        nc = NATS()
        await nc.connect(f"nats://{host}:{port}")
        async def handler(msg):
            messages.append({"subject": msg.subject, "data": msg.data.decode()})
        await nc.subscribe(subject, handler=handler)
        await asyncio.sleep(max_messages * 0.5)
        await nc.close()
    asyncio.run(_sub())
    return {"subject": subject, "messages": messages, "count": len(messages)}


def nats_jetstream_info_cmd(host: str = "localhost", port: int = 4222) -> Dict:
    if not NATS_AVAILABLE:
        raise ImportError("nats-py not installed. Run: pip install nats-py")
    info = {}
    async def _info():
        nonlocal info
        nc = NATS()
        await nc.connect(f"nats://{host}:{port}")
        js = nc.jetstream()
        info = {"status": "connected", "streams": "via js"}
        await nc.close()
    asyncio.run(_info())
    return info


def register(plugin):
    plugin.register_command("publish", nats_publish_cmd)
    plugin.register_command("subscribe", nats_subscribe_cmd)
    plugin.register_command("jetstream_info", nats_jetstream_info_cmd)


PLUGIN_METADATA = {
    "name": "nats_ops", "version": "1.0.0",
    "description": "NATS.io publish/subscribe messaging",
    "author": "Mito Team", "license": "MIT",
    "tags": ["nats", "messaging", "streaming", "devops"],
    "dependencies": ["nats-py"], "permissions": ["nats_access"],
    "min_mito_version": "1.0.1",
}

nats_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
