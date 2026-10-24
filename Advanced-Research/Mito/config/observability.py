"""
Mito Observability - Metrics, Rate Limiting, Security
"""

import time
import hashlib
from typing import Dict, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import threading
from prometheus_client import Counter, Histogram, Gauge, generate_latest


METRICS = {
    "requests": Counter("mito_requests_total", "Total requests", ["endpoint", "method"]),
    "latency": Histogram("mito_request_latency_seconds", "Request latency", ["endpoint"]),
    "errors": Counter("mito_errors_total", "Total errors", ["endpoint", "error_type"]),
    "inference": Histogram("mito_inference_seconds", "Inference time", ["model"]),
    "tokens": Counter("mito_tokens_total", "Tokens generated", ["model"]),
    "active_models": Gauge("mito_active_models", "Active models"),
}


class RateLimiter:
    """Token bucket rate limiter."""
    
    def __init__(self, rate: int = 100, period: int = 60):
        self.rate = rate
        self.period = period
        self.buckets: Dict[str, Dict] = defaultdict(lambda: {"tokens": rate, "last": time.time()})
        self.lock = threading.Lock()
    
    def allow(self, key: str) -> bool:
        with self.lock:
            bucket = self.buckets[key]
            now = time.time()
            
            elapsed = now - bucket["last"]
            bucket["tokens"] = min(self.rate, bucket["tokens"] + elapsed * (self.rate / self.period))
            bucket["last"] = now
            
            if bucket["tokens"] >= 1:
                bucket["tokens"] -= 1
                return True
            return False
    
    def get_remaining(self, key: str) -> int:
        return int(self.buckets[key]["tokens"])
    
    def reset(self, key: str):
        with self.lock:
            self.buckets[key] = {"tokens": self.rate, "last": time.time()}


class APIKeyManager:
    """Manage API keys."""
    
    def __init__(self):
        self.keys: Dict[str, Dict] = {}
    
    def create_key(self, name: str, rate_limit: int = 100) -> str:
        key = hashlib.sha256(f"{name}{time.time()}".encode()).hexdigest()[:32]
        self.keys[key] = {
            "name": name,
            "rate_limit": rate_limit,
            "created_at": datetime.now(),
            "requests": 0
        }
        return key
    
    def validate_key(self, key: str) -> bool:
        return key in self.keys
    
    def get_key_info(self, key: str) -> Optional[Dict]:
        return self.keys.get(key)
    
    def delete_key(self, key: str):
        if key in self.keys:
            del self.keys[key]
    
    def list_keys(self) -> Dict[str, str]:
        return {k: v["name"] for k, v in self.keys.items()}


class RequestLogger:
    """Log all requests."""
    
    def __init__(self):
        self.requests: list = []
        self.lock = threading.Lock()
        self.max_size = 10000
    
    def log(self, method: str, path: str, status: int, duration: float):
        with self.lock:
            self.requests.append({
                "timestamp": datetime.now().isoformat(),
                "method": method,
                "path": path,
                "status": status,
                "duration": duration
            })
            if len(self.requests) > self.max_size:
                self.requests = self.requests[-self.max_size:]
    
    def get_recent(self, limit: int = 100) -> list:
        return self.requests[-limit:]
    
    def get_stats(self) -> Dict:
        if not self.requests:
            return {"total": 0}
        
        return {
            "total": len(self.requests),
            "avg_duration": sum(r["duration"] for r in self.requests) / len(self.requests),
            "by_status": defaultdict(int),
            "by_method": defaultdict(int)
        }


def require_api_key(get_key: Callable[[], Optional[str]], manager: APIKeyManager):
    """Decorator to require API key."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = get_key()
            if not key or not manager.validate_key(key):
                raise PermissionError("Invalid API key")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def rate_limit(get_key: Callable[[], Optional[str]], limiter: RateLimiter):
    """Decorator for rate limiting."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = get_key() or "default"
            if not limiter.allow(key):
                raise Exception("429 Rate limit exceeded")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def track_metrics(endpoint: str, method: str = "GET"):
    """Decorator to track metrics."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                METRICS["requests"].labels(endpoint=endpoint, method=method).inc()
                return result
            except Exception as e:
                METRICS["errors"].labels(endpoint=endpoint, error_type=type(e).__name__).inc()
                raise
            finally:
                duration = time.time() - start
                METRICS["latency"].labels(endpoint=endpoint).observe(duration)
        return wrapper
    return decorator


def get_metrics() -> str:
    """Get Prometheus metrics."""
    return generate_latest()


if __name__ == '__main__':
    limiter = RateLimiter(rate=10, period=60)
    for i in range(15):
        print(f"Request {i+1}: {limiter.allow('test')}")
    
    manager = APIKeyManager()
    key = manager.create_key("test-user")
    print(f"Created key: {key}")
    print(f"Valid: {manager.validate_key(key)}")
