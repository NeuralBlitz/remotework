from __future__ import annotations

import functools
import signal
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

from pg_batchgov.models import BatchConfig, Priority

P = ParamSpec("P")
R = TypeVar("R")


class LowPriorityDecorator:
    def __init__(self, config: BatchConfig) -> None:
        self.config = config
        self._original_func: Callable[..., Any] | None = None

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        self._original_func = func

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if self.config.priority == Priority.LOW:
                pass
            return func(*args, **kwargs)

        wrapper._batch_config = self.config  # type: ignore[attr-defined]
        wrapper._original_func = func  # type: ignore[attr-defined]
        return wrapper


class TimeoutDecorator:
    def __init__(self, timeout_seconds: float) -> None:
        self.timeout_seconds = timeout_seconds

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            def timeout_handler(_signum: int, _frame: Any) -> None:
                raise TimeoutError(
                    f"Function {func.__name__} exceeded timeout of {self.timeout_seconds}s"
                )

            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.setitimer(signal.ITIMER_REAL, self.timeout_seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
                signal.signal(signal.SIGALRM, old_handler)
            return result

        wrapper._timeout_seconds = self.timeout_seconds  # type: ignore[attr-defined]
        return wrapper


class RetryDecorator:
    def __init__(self, max_retries: int = 3) -> None:
        self.max_retries = max_retries

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_error: Exception | None = None
            for attempt in range(self.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
                    if attempt == self.max_retries:
                        raise
            raise last_error  # type: ignore[misc]

        wrapper._max_retries = self.max_retries  # type: ignore[attr-defined]
        return wrapper
