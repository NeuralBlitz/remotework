"""
Mito Server Middleware
CORS, auth, rate limiting, logging, error handling, request ID
"""

import time
import uuid
import logging
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass

logger = logging.getLogger("mito.middleware")


@dataclass
class MiddlewareContext:
    request_id: str
    path: str
    method: str
    headers: Dict[str, str]
    start_time: float
    metadata: Dict[str, Any]


class CORSMiddleware:
    def __init__(self, allow_origins: List[str] = None, allow_methods: List[str] = None,
                 allow_headers: List[str] = None, max_age: int = 86400):
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.allow_headers = allow_headers or ["*"]
        self.max_age = max_age

    def process_request(self, ctx: MiddlewareContext) -> Optional[Dict]:
        if ctx.method == "OPTIONS":
            return {
                "status": 204,
                "headers": {
                    "Access-Control-Allow-Origin": ", ".join(self.allow_origins),
                    "Access-Control-Allow-Methods": ", ".join(self.allow_methods),
                    "Access-Control-Allow-Headers": ", ".join(self.allow_headers),
                    "Access-Control-Max-Age": str(self.max_age),
                },
            }
        return None

    def process_response(self, ctx: MiddlewareContext, response: Dict) -> Dict:
        headers = response.get("headers", {})
        headers["Access-Control-Allow-Origin"] = ", ".join(self.allow_origins)
        response["headers"] = headers
        return response


class AuthMiddleware:
    def __init__(self, api_keys: List[str] = None, token_prefix: str = "Bearer",
                 exempt_paths: List[str] = None):
        self.api_keys = set(api_keys or [])
        self.token_prefix = token_prefix
        self.exempt_paths = set(exempt_paths or ["/health", "/docs", "/openapi.json"])

    def process_request(self, ctx: MiddlewareContext) -> Optional[Dict]:
        if ctx.path in self.exempt_paths:
            return None

        auth = ctx.headers.get("Authorization", "")
        if auth.startswith(f"{self.token_prefix} "):
            token = auth[len(self.token_prefix) + 1:]
            if token in self.api_keys or not self.api_keys:
                return None

        api_key = ctx.headers.get("X-API-Key", "")
        if api_key in self.api_keys or not self.api_keys:
            return None

        return {"status": 401, "body": {"error": "Unauthorized"}}


class RateLimitMiddleware:
    def __init__(self, rate: int = 100, period: int = 60, key_func: Callable = None):
        self.rate = rate
        self.period = period
        self.key_func = key_func or (lambda ctx: ctx.headers.get("X-Forwarded-For", "default"))
        self._buckets: Dict[str, List[float]] = {}

    def process_request(self, ctx: MiddlewareContext) -> Optional[Dict]:
        key = self.key_func(ctx)
        now = time.time()

        if key not in self._buckets:
            self._buckets[key] = []

        self._buckets[key] = [t for t in self._buckets[key] if now - t < self.period]

        if len(self._buckets[key]) >= self.rate:
            return {
                "status": 429,
                "body": {"error": "Rate limit exceeded"},
                "headers": {
                    "X-RateLimit-Limit": str(self.rate),
                    "X-RateLimit-Remaining": "0",
                    "Retry-After": str(self.period),
                },
            }

        self._buckets[key].append(now)
        return None


class RequestIDMiddleware:
    def __init__(self, header_name: str = "X-Request-ID"):
        self.header_name = header_name

    def process_request(self, ctx: MiddlewareContext) -> Optional[Dict]:
        if self.header_name.lower() not in {k.lower() for k in ctx.headers}:
            ctx.request_id = str(uuid.uuid4())
        return None

    def process_response(self, ctx: MiddlewareContext, response: Dict) -> Dict:
        headers = response.get("headers", {})
        headers[self.header_name] = ctx.request_id
        response["headers"] = headers
        return response


class LoggingMiddleware:
    def __init__(self, log_body: bool = False):
        self.log_body = log_body

    def process_request(self, ctx: MiddlewareContext) -> Optional[Dict]:
        logger.info(f"[{ctx.request_id}] {ctx.method} {ctx.path}")
        return None

    def process_response(self, ctx: MiddlewareContext, response: Dict) -> Dict:
        duration = (time.time() - ctx.start_time) * 1000
        status = response.get("status", 200)
        logger.info(f"[{ctx.request_id}] {ctx.method} {ctx.path} -> {status} ({duration:.1f}ms)")
        return response


class ErrorHandlingMiddleware:
    def process_error(self, ctx: MiddlewareContext, error: Exception) -> Dict:
        logger.error(f"[{ctx.request_id}] Error: {error}")
        return {
            "status": 500,
            "body": {"error": "Internal server error", "request_id": ctx.request_id},
        }


class CompressionMiddleware:
    def __init__(self, min_size: int = 1024):
        self.min_size = min_size

    def process_response(self, ctx: MiddlewareContext, response: Dict) -> Dict:
        body = response.get("body", "")
        if isinstance(body, str) and len(body) > self.min_size:
            headers = response.get("headers", {})
            headers["Content-Encoding"] = "gzip"
            response["headers"] = headers
        return response


class SecurityHeadersMiddleware:
    def process_response(self, ctx: MiddlewareContext, response: Dict) -> Dict:
        headers = response.get("headers", {})
        headers.update({
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
        })
        response["headers"] = headers
        return response


class MiddlewareStack:
    def __init__(self):
        self.middlewares: List[Any] = []

    def add(self, middleware: Any) -> "MiddlewareStack":
        self.middlewares.append(middleware)
        return self

    def process_request(self, ctx: MiddlewareContext) -> Optional[Dict]:
        for mw in self.middlewares:
            if hasattr(mw, "process_request"):
                result = mw.process_request(ctx)
                if result is not None:
                    return result
        return None

    def process_response(self, ctx: MiddlewareContext, response: Dict) -> Dict:
        for mw in reversed(self.middlewares):
            if hasattr(mw, "process_response"):
                response = mw.process_response(ctx, response)
        return response

    def process_error(self, ctx: MiddlewareContext, error: Exception) -> Dict:
        for mw in self.middlewares:
            if hasattr(mw, "process_error"):
                return mw.process_error(ctx, error)
        return {"status": 500, "body": {"error": str(error)}}
