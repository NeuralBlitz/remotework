"""
Redis Integration Plugin
Cache, pub/sub, key-value operations via Redis
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Callable

logger = logging.getLogger("mito.plugins.redis")


class RedisClient:
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None,
                 password: Optional[str] = None, db: int = 0):
        self.host = host or os.environ.get("REDIS_HOST", "localhost")
        self.port = port or int(os.environ.get("REDIS_PORT", "6379"))
        self.password = password or os.environ.get("REDIS_PASSWORD", "")
        self.db = db
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                import redis
                self._client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    password=self.password,
                    db=self.db,
                    decode_responses=True,
                    socket_timeout=5,
                )
                self._client.ping()
            except ImportError:
                raise ImportError("redis not installed. Install with: pip install redis")
            except Exception as e:
                raise ConnectionError(f"Cannot connect to Redis at {self.host}:{self.port}: {e}")
        return self._client

    def get(self, key: str) -> Optional[str]:
        client = self._get_client()
        return client.get(key)

    def set(self, key: str, value: str, ex: int = None) -> bool:
        client = self._get_client()
        return client.set(key, value, ex=ex)

    def delete(self, key: str) -> bool:
        client = self._get_client()
        return bool(client.delete(key))

    def exists(self, key: str) -> bool:
        client = self._get_client()
        return bool(client.exists(key))

    def keys(self, pattern: str = "*") -> List[str]:
        client = self._get_client()
        return client.keys(pattern)

    def hset(self, name: str, key: str, value: str) -> int:
        client = self._get_client()
        return client.hset(name, key, value)

    def hget(self, name: str, key: str) -> Optional[str]:
        client = self._get_client()
        return client.hget(name, key)

    def hgetall(self, name: str) -> Dict[str, str]:
        client = self._get_client()
        return client.hgetall(name)

    def lpush(self, name: str, *values) -> int:
        client = self._get_client()
        return client.lpush(name, *values)

    def rpush(self, name: str, *values) -> int:
        client = self._get_client()
        return client.rpush(name, *values)

    def lrange(self, name: str, start: int = 0, end: int = -1) -> List[str]:
        client = self._get_client()
        return client.lrange(name, start, end)

    def publish(self, channel: str, message: str) -> int:
        client = self._get_client()
        return client.publish(channel, message)

    def subscribe(self, channel: str, callback: Callable):
        client = self._get_client()
        pubsub = client.pubsub()
        pubsub.subscribe(channel)
        for message in pubsub.listen():
            if message["type"] == "message":
                callback(message["data"])

    def flush(self) -> bool:
        client = self._get_client()
        client.flushdb()
        return True

    def info(self) -> Dict:
        client = self._get_client()
        return client.info()

    def ttl(self, key: str) -> int:
        client = self._get_client()
        return client.ttl(key)

    def incr(self, key: str) -> int:
        client = self._get_client()
        return client.incr(key)

    def decr(self, key: str) -> int:
        client = self._get_client()
        return client.decr(key)

    def set_json(self, key: str, value: Any, ex: int = None) -> bool:
        return self.set(key, json.dumps(value), ex=ex)

    def get_json(self, key: str) -> Any:
        val = self.get(key)
        return json.loads(val) if val else None


def redis_get_cmd(key: str = "") -> Optional[str]:
    """Get a value from Redis."""
    client = RedisClient()
    return client.get(key)


def redis_set_cmd(key: str = "", value: str = "", ttl: int = 0) -> bool:
    """Set a value in Redis."""
    client = RedisClient()
    return client.set(key, value, ex=ttl if ttl > 0 else None)


def redis_keys_cmd(pattern: str = "*") -> List[str]:
    """List Redis keys matching a pattern."""
    client = RedisClient()
    return client.keys(pattern)


def redis_delete_cmd(key: str = "") -> bool:
    """Delete a key from Redis."""
    client = RedisClient()
    return client.delete(key)


def register(plugin):
    plugin.register_command("redis_get", redis_get_cmd)
    plugin.register_command("redis_set", redis_set_cmd)
    plugin.register_command("redis_keys", redis_keys_cmd)
    plugin.register_command("redis_delete", redis_delete_cmd)
    plugin.set_resource("client_class", RedisClient)


PLUGIN_METADATA = {
    "name": "redis",
    "version": "1.0.0",
    "description": "Redis integration - Cache, pub/sub, key-value store",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["redis", "cache", "pubsub", "database"],
    "dependencies": ["redis"],
    "permissions": ["network_access", "read_env"],
    "min_mito_version": "1.0.0",
}


redis_plugin = {
    "metadata": PLUGIN_METADATA,
    "register": register,
}
