"""
Pulsar Operations Plugin
Apache Pulsar produce and consume messaging.
"""
import logging
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.pulsar_ops")

try:
    import pulsar
    PULSAR_AVAILABLE = True
except ImportError:
    PULSAR_AVAILABLE = False


def pulsar_produce_cmd(topic: str = "", message: str = "", service_url: str = "pulsar://localhost:6650") -> Dict:
    if not PULSAR_AVAILABLE:
        raise ImportError("pulsar not installed. Run: pip install pulsar-client")
    client = pulsar.Client(service_url)
    producer = client.create_producer(topic)
    producer.send(message.encode())
    client.close()
    return {"topic": topic, "message": message[:100], "status": "produced"}


def pulsar_consume_cmd(topic: str = "", subscription: str = "mito-sub", service_url: str = "pulsar://localhost:6650",
                       max_messages: int = 10) -> Dict:
    if not PULSAR_AVAILABLE:
        raise ImportError("pulsar not installed. Run: pip install pulsar-client")
    client = pulsar.Client(service_url)
    consumer = client.subscribe(topic, subscription)
    messages = []
    for i in range(max_messages):
        msg = consumer.receive(timeout_millis=5000)
        if msg:
            messages.append({"data": msg.data().decode(), "message_id": str(msg.message_id())})
            consumer.acknowledge(msg)
    client.close()
    return {"topic": topic, "messages": messages, "count": len(messages)}


def pulsar_list_topics_cmd(service_url: str = "pulsar://localhost:6650") -> Dict:
    if not PULSAR_AVAILABLE:
        raise ImportError("pulsar not installed. Run: pip install pulsar-client")
    client = pulsar.Client(service_url)
    topics = client.get_topics()
    client.close()
    return {"topics": topics, "count": len(topics)}


def pulsar_create_subscription_cmd(topic: str = "", subscription: str = "", service_url: str = "pulsar://localhost:6650") -> Dict:
    if not PULSAR_AVAILABLE:
        raise ImportError("pulsar not installed. Run: pip install pulsar-client")
    client = pulsar.Client(service_url)
    consumer = client.subscribe(topic, subscription)
    client.close()
    return {"topic": topic, "subscription": subscription, "status": "created"}


def register(plugin):
    plugin.register_command("produce", pulsar_produce_cmd)
    plugin.register_command("consume", pulsar_consume_cmd)
    plugin.register_command("list_topics", pulsar_list_topics_cmd)
    plugin.register_command("create_subscription", pulsar_create_subscription_cmd)


PLUGIN_METADATA = {
    "name": "pulsar_ops", "version": "1.0.0",
    "description": "Apache Pulsar produce, consume, and topic management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["pulsar", "messaging", "streaming", "devops"],
    "dependencies": ["pulsar-client"], "permissions": ["pulsar_access"],
    "min_mito_version": "1.0.1",
}

pulsar_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
