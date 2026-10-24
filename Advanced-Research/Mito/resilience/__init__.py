"""
Mito Resilience Patterns
Circuit breaker, retry, bulkhead, timeout, fallback
"""

import time
import logging
import threading
import functools
from typing import Dict, List, Optional, Any, Callable, Type
from dataclasses import dataclass, field
from enum import Enum
from collections import deque

logger = logging.getLogger("mito.resilience")


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    expected_exceptions: tuple = (Exception,)
    success_threshold: int = 3
    monitor_window: float = 60.0


class CircuitBreaker:
    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0
        self.last_exception = None
        self._lock = threading.Lock()
        self._history: deque = deque(maxlen=100)

    def call(self, func: Callable, *args, **kwargs) -> Any:
        with self._lock:
            if self.state == CircuitState.OPEN:
                if time.time() - self.last_failure_time > self.config.recovery_timeout:
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                    logger.info(f"Circuit '{self.name}' entering half-open state")
                else:
                    raise Exception(f"Circuit '{self.name}' is OPEN - calls blocked")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.config.expected_exceptions as e:
            self._on_failure(e)
            raise

    def _on_success(self):
        with self._lock:
            self._history.append({"time": time.time(), "success": True})
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.config.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    logger.info(f"Circuit '{self.name}' closed - recovered")
            else:
                self.failure_count = max(0, self.failure_count - 1)

    def _on_failure(self, exception: Exception):
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            self.last_exception = str(exception)
            self._history.append({"time": time.time(), "success": False, "error": str(exception)})

            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                logger.warning(f"Circuit '{self.name}' reopened after half-open failure")
            elif self.failure_count >= self.config.failure_threshold:
                self.state = CircuitState.OPEN
                logger.warning(f"Circuit '{self.name}' opened after {self.failure_count} failures")

    def get_stats(self) -> Dict:
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure_time": self.last_failure_time,
            "last_exception": self.last_exception,
        }

    def reset(self):
        with self._lock:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.success_count = 0
            self.last_failure_time = 0
            self.last_exception = None


def circuit_breaker(name: str, config: CircuitBreakerConfig = None):
    """Decorator for circuit breaker pattern."""
    cb = CircuitBreaker(name, config)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return cb.call(func, *args, **kwargs)
        wrapper.circuit_breaker = cb
        return wrapper
    return decorator


class RetryPolicy:
    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0,
                 max_delay: float = 30.0, exponential: bool = True,
                 jitter: bool = True, retry_on: tuple = (Exception,)):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential = exponential
        self.jitter = jitter
        self.retry_on = retry_on

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        import random
        last_exception = None

        for attempt in range(1, self.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except self.retry_on as e:
                last_exception = e
                if attempt == self.max_attempts:
                    raise

                delay = self.base_delay
                if self.exponential:
                    delay = min(self.base_delay * (2 ** (attempt - 1)), self.max_delay)
                if self.jitter:
                    delay *= (0.5 + random.random() * 0.5)

                logger.warning(f"Retry {attempt}/{self.max_attempts} after {delay:.1f}s: {e}")
                time.sleep(delay)

        raise last_exception


def retry(max_attempts: int = 3, base_delay: float = 1.0, exponential: bool = True):
    """Decorator for retry with exponential backoff."""
    policy = RetryPolicy(max_attempts=max_attempts, base_delay=base_delay, exponential=exponential)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return policy.execute(func, *args, **kwargs)
        wrapper.retry_policy = policy
        return wrapper
    return decorator


class Bulkhead:
    """Limits concurrent calls to a resource."""

    def __init__(self, name: str, max_concurrent: int = 10, max_wait: float = 0):
        self.name = name
        self.max_concurrent = max_concurrent
        self.max_wait = max_wait
        self.semaphore = threading.Semaphore(max_concurrent)
        self.active = 0
        self.rejected = 0
        self._lock = threading.Lock()

    def call(self, func: Callable, *args, **kwargs) -> Any:
        acquired = self.semaphore.acquire(timeout=self.max_wait if self.max_wait > 0 else None)
        if not acquired:
            with self._lock:
                self.rejected += 1
            raise Exception(f"Bulkhead '{self.name}' full - call rejected")
        try:
            with self._lock:
                self.active += 1
            return func(*args, **kwargs)
        finally:
            with self._lock:
                self.active -= 1
            self.semaphore.release()

    def get_stats(self) -> Dict:
        return {
            "name": self.name,
            "max_concurrent": self.max_concurrent,
            "active": self.active,
            "rejected": self.rejected,
        }


def bulkhead(name: str, max_concurrent: int = 10):
    """Decorator for bulkhead pattern."""
    bh = Bulkhead(name, max_concurrent)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return bh.call(func, *args, **kwargs)
        wrapper.bulkhead = bh
        return wrapper
    return decorator


class Timeout:
    """Timeout wrapper for functions."""

    def __init__(self, seconds: float):
        self.seconds = seconds

    def call(self, func: Callable, *args, **kwargs) -> Any:
        from concurrent.futures import ThreadPoolExecutor, TimeoutError as FETimeout
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args, **kwargs)
            try:
                return future.result(timeout=self.seconds)
            except FETimeout:
                raise TimeoutError(f"Function timed out after {self.seconds}s")


def timeout(seconds: float):
    """Decorator for timeout."""
    t = Timeout(seconds)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return t.call(func, *args, **kwargs)
        return wrapper
    return decorator


class FallbackChain:
    """Try multiple functions, falling back on failure."""

    def __init__(self, functions: List[Callable], exceptions: tuple = (Exception,)):
        self.functions = functions
        self.exceptions = exceptions

    def execute(self, *args, **kwargs) -> Any:
        last_exception = None
        for func in self.functions:
            try:
                return func(*args, **kwargs)
            except self.exceptions as e:
                last_exception = e
                logger.debug(f"Fallback {func.__name__} failed: {e}")
        raise last_exception


def fallback(*functions):
    """Decorator for fallback chain."""
    chain = FallbackChain(list(functions))

    def decorator(func):
        all_funcs = [func] + list(functions)
        fc = FallbackChain(all_funcs)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return fc.execute(*args, **kwargs)
        return wrapper
    return decorator
