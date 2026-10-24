"""
RabbitMQ Operations Plugin
Publish and consume messages via RabbitMQ.
"""
import logging
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.rabbitmq_ops")

try:
    import pika
    RMQ_AVAILABLE = True
except ImportError:
    RMQ_AVAILABLE = False


def _connection(host: str = "localhost", port: int = 5672, user: str = "guest", password: str = "guest"):
    if not RMQ_AVAILABLE:
        raise ImportError("pika not installed. Run: pip install pika")
    creds = pika.PlainCredentials(user, password)
    params = pika.ConnectionParameters(host=host, port=port, credentials=creds)
    return pika.BlockingConnection(params)


def rabbitmq_publish_cmd(queue: str = "", message: str = "", host: str = "localhost", 
                         port: int = 5672, user: str = "guest", password: str = "guest") -> Dict:
    conn = _connection(host, port, user, password)
    channel = conn.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(exchange="", routing_key=queue, body=message)
    conn.close()
    return {"queue": queue, "message": message[:100], "status": "published"}


def rabbitmq_consume_cmd(queue: str = "", host: str = "localhost", port: int = 5672,
                         user: str = "guest", password: str = "guest", max_messages: int = 10) -> Dict:
    conn = _connection(host, port, user, password)
    channel = conn.channel()
    channel.queue_declare(queue=queue, durable=True)
    messages = []
    for i in range(max_messages):
        method, props, body = channel.basic_get(queue=queue, auto_ack=True)
        if method:
            messages.append({"body": body.decode(), "delivery_tag": method.delivery_tag})
        else:
            break
    conn.close()
    return {"queue": queue, "messages": messages, "count": len(messages)}


def rabbitmq_declare_queue_cmd(queue: str = "", host: str = "localhost", port: int = 5672,
                                user: str = "guest", password: str = "guest", durable: bool = True) -> Dict:
    conn = _connection(host, port, user, password)
    channel = conn.channel()
    channel.queue_declare(queue=queue, durable=durable)
    conn.close()
    return {"queue": queue, "status": "declared"}


def rabbitmq_declare_exchange_cmd(exchange: str = "", exchange_type: str = "direct",
                                  host: str = "localhost", port: int = 5672,
                                  user: str = "guest", password: str = "guest") -> Dict:
    conn = _connection(host, port, user, password)
    channel = conn.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    conn.close()
    return {"exchange": exchange, "type": exchange_type, "status": "declared"}


def rabbitmq_list_queues_cmd(host: str = "localhost", port: int = 5672,
                              user: str = "guest", password: str = "guest") -> Dict:
    conn = _connection(host, port, user, password)
    channel = conn.channel()
    queues = channel.queue_declare(queue="", passive=True)
    result = channel.queue_declare(passive=True)
    conn.close()
    return {"queues": [{"name": r.method.queue, "messages": r.method.message_count} for r in [result]]}


def register(plugin):
    plugin.register_command("publish", rabbitmq_publish_cmd)
    plugin.register_command("consume", rabbitmq_consume_cmd)
    plugin.register_command("declare_queue", rabbitmq_declare_queue_cmd)
    plugin.register_command("declare_exchange", rabbitmq_declare_exchange_cmd)
    plugin.register_command("list_queues", rabbitmq_list_queues_cmd)


PLUGIN_METADATA = {
    "name": "rabbitmq_ops", "version": "1.0.0",
    "description": "RabbitMQ publish, consume, and queue management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["rabbitmq", "messaging", "amqp", "devops"],
    "dependencies": ["pika"], "permissions": ["rabbitmq_access"],
    "min_mito_version": "1.0.1",
}

rabbitmq_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
