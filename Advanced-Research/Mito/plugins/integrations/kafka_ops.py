"""
Kafka Operations Plugin
Produce and consume messages via Apache Kafka.
"""
import logging
import json
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.kafka_ops")

try:
    from kafka import KafkaProducer, KafkaConsumer
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False


def kafka_produce_cmd(topic: str = "", message: str = "", bootstrap: str = "localhost:9092") -> Dict:
    if not KAFKA_AVAILABLE:
        raise ImportError("kafka-python not installed. Run: pip install kafka-python")
    producer = KafkaProducer(bootstrap_servers=bootstrap, value_serializer=lambda v: json.dumps(v).encode())
    future = producer.send(topic, value=message)
    producer.flush()
    record = future.get(timeout=10)
    return {"topic": topic, "partition": record.partition, "offset": record.offset, "status": "produced"}


def kafka_consume_cmd(topic: str = "", bootstrap: str = "localhost:9092", group_id: str = "mito-group",
                      max_messages: int = 10) -> Dict:
    if not KAFKA_AVAILABLE:
        raise ImportError("kafka-python not installed. Run: pip install kafka-python")
    consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap, group_id=group_id,
                           value_deserializer=lambda m: json.loads(m.decode()),
                           auto_offset_reset="earliest", max_poll_records=max_messages)
    messages = []
    for i, msg in enumerate(consumer):
        if i >= max_messages:
            break
        messages.append({"topic": msg.topic, "partition": msg.partition, "offset": msg.offset, "value": msg.value})
    consumer.close()
    return {"messages": messages, "count": len(messages)}


def kafka_list_topics_cmd(bootstrap: str = "localhost:9092") -> Dict:
    if not KAFKA_AVAILABLE:
        raise ImportError("kafka-python not installed. Run: pip install kafka-python")
    from kafka import KafkaAdminClient
    admin = KafkaAdminClient(bootstrap_servers=bootstrap)
    topics = admin.list_topics()
    return {"topics": topics, "count": len(topics)}


def kafka_create_topic_cmd(topic: str = "", partitions: int = 1, replication: int = 1,
                           bootstrap: str = "localhost:9092") -> Dict:
    if not KAFKA_AVAILABLE:
        raise ImportError("kafka-python not installed. Run: pip install kafka-python")
    from kafka.admin import NewTopic
    admin = KafkaAdminClient(bootstrap_servers=bootstrap)
    admin.create_topics([NewTopic(topic, num_partitions=partitions, replication_factor=replication)])
    return {"topic": topic, "partitions": partitions, "replication": replication, "status": "created"}


def kafka_get_offsets_cmd(topic: str = "", bootstrap: str = "localhost:9092") -> Dict:
    if not KAFKA_AVAILABLE:
        raise ImportError("kafka-python not installed. Run: pip install kafka-python")
    from kafka import KafkaConsumer
    consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap, auto_offset_reset="earliest")
    partitions = consumer.assignment()
    offsets = {}
    for p in partitions:
        lo, hi = consumer.beginning_offsets([p])[p]
        offsets[str(p)] = {"begin": lo, "end": hi}
    consumer.close()
    return {"topic": topic, "partitions": offsets}


def register(plugin):
    plugin.register_command("produce", kafka_produce_cmd)
    plugin.register_command("consume", kafka_consume_cmd)
    plugin.register_command("list_topics", kafka_list_topics_cmd)
    plugin.register_command("create_topic", kafka_create_topic_cmd)
    plugin.register_command("get_offsets", kafka_get_offsets_cmd)


PLUGIN_METADATA = {
    "name": "kafka_ops", "version": "1.0.0",
    "description": "Apache Kafka produce, consume, and topic management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["kafka", "messaging", "streaming", "devops"],
    "dependencies": ["kafka-python"], "permissions": ["kafka_access"],
    "min_mito_version": "1.0.1",
}

kafka_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
