"""
Mito Health Checks
Liveness, readiness probes, dependency checks, system metrics
"""

import time
import logging
import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger("mito.health")


class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass
class CheckResult:
    name: str
    status: HealthStatus
    message: str
    duration_ms: float
    timestamp: float
    details: Dict[str, Any] = field(default_factory=dict)


class HealthCheck:
    def __init__(self, name: str, check_func: Callable, critical: bool = True,
                 timeout: float = 5.0, tags: List[str] = None):
        self.name = name
        self.check_func = check_func
        self.critical = critical
        self.timeout = timeout
        self.tags = tags or []
        self.last_result: Optional[CheckResult] = None

    def run(self) -> CheckResult:
        start = time.time()
        try:
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(self.check_func)
                result = future.result(timeout=self.timeout)

            duration = (time.time() - start) * 1000
            if isinstance(result, dict):
                status = HealthStatus(result.get("status", "healthy"))
                message = result.get("message", "OK")
                details = result.get("details", {})
            else:
                status = HealthStatus.HEALTHY
                message = str(result) if result else "OK"
                details = {}

            check = CheckResult(self.name, status, message, duration, time.time(), details)
        except Exception as e:
            duration = (time.time() - start) * 1000
            check = CheckResult(
                self.name, HealthStatus.UNHEALTHY, str(e), duration, time.time()
            )

        self.last_result = check
        return check


class HealthRegistry:
    def __init__(self):
        self.checks: Dict[str, HealthCheck] = {}

    def register(self, name: str, check_func: Callable, critical: bool = True,
                 timeout: float = 5.0, tags: List[str] = None) -> HealthCheck:
        check = HealthCheck(name, check_func, critical, timeout, tags)
        self.checks[name] = check
        return check

    def unregister(self, name: str):
        self.checks.pop(name, None)

    def run_all(self, tags: List[str] = None) -> Dict[str, CheckResult]:
        results = {}
        for name, check in self.checks.items():
            if tags and not set(tags) & set(check.tags):
                continue
            results[name] = check.run()
        return results

    def get_status(self, tags: List[str] = None) -> HealthStatus:
        results = self.run_all(tags)
        statuses = [r.status for r in results.values()]

        if any(s == HealthStatus.UNHEALTHY for s in statuses):
            return HealthStatus.UNHEALTHY
        if any(s == HealthStatus.DEGRADED for s in statuses):
            return HealthStatus.DEGRADED
        return HealthStatus.HEALTHY

    def get_report(self, tags: List[str] = None) -> Dict:
        results = self.run_all(tags)
        critical_checks = {n: r for n, r in results.items() if self.checks[n].critical}

        return {
            "status": self.get_status(tags).value,
            "timestamp": time.time(),
            "checks": {n: {
                "status": r.status.value,
                "message": r.message,
                "duration_ms": r.duration_ms,
                "details": r.details,
            } for n, r in results.items()},
            "summary": {
                "total": len(results),
                "healthy": sum(1 for r in results.values() if r.status == HealthStatus.HEALTHY),
                "degraded": sum(1 for r in results.values() if r.status == HealthStatus.DEGRADED),
                "unhealthy": sum(1 for r in results.values() if r.status == HealthStatus.UNHEALTHY),
                "critical_unhealthy": sum(
                    1 for n, r in critical_checks.items() if r.status == HealthStatus.UNHEALTHY
                ),
            },
        }


# Built-in checks
def check_disk_space(path: str = "/", min_free_gb: float = 1.0) -> Dict:
    import shutil
    total, used, free = shutil.disk_usage(path)
    free_gb = free / (1024**3)
    if free_gb < min_free_gb:
        return {"status": "unhealthy", "message": f"Low disk: {free_gb:.1f}GB free"}
    return {"status": "healthy", "message": f"Disk OK: {free_gb:.1f}GB free"}


def check_memory(min_free_mb: float = 100.0) -> Dict:
    import psutil
    mem = psutil.virtual_memory()
    available_mb = mem.available / (1024**2)
    if available_mb < min_free_mb:
        return {"status": "unhealthy", "message": f"Low memory: {available_mb:.0f}MB available"}
    pct = mem.percent
    if pct > 90:
        return {"status": "degraded", "message": f"Memory usage high: {pct:.0f}%"}
    return {"status": "healthy", "message": f"Memory OK: {pct:.0f}% used", "details": {"percent": pct}}


def check_url(url: str, timeout: float = 5.0) -> Dict:
    import requests
    try:
        resp = requests.get(url, timeout=timeout)
        if resp.ok:
            return {"status": "healthy", "message": f"URL OK: {resp.status_code}"}
        return {"status": "unhealthy", "message": f"URL returned {resp.status_code}"}
    except Exception as e:
        return {"status": "unhealthy", "message": f"URL unreachable: {e}"}


def check_port(host: str, port: int, timeout: float = 3.0) -> Dict:
    import socket
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        return {"status": "healthy", "message": f"Port {port} open"}
    except Exception as e:
        return {"status": "unhealthy", "message": f"Port {port} closed: {e}"}


# Global registry
_global_registry: Optional[HealthRegistry] = None


def get_health_registry() -> HealthRegistry:
    global _global_registry
    if _global_registry is None:
        _global_registry = HealthRegistry()
    return _global_registry
