"""
Mito Audit Log
Immutable audit trail with query builder, export, retention, and compliance
"""

import json
import logging
import time
import uuid
import csv
import io
import hashlib
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from datetime import datetime, timedelta
import threading

logger = logging.getLogger("mito.audit")


class AuditLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditCategory(Enum):
    AUTH = "auth"
    DATA = "data"
    SYSTEM = "system"
    USER = "user"
    API = "api"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    INTEGRATION = "integration"


@dataclass
class AuditEntry:
    id: str
    action: str
    actor: str
    resource: str
    resource_id: str
    level: AuditLevel
    timestamp: float
    category: AuditCategory = AuditCategory.SYSTEM
    details: Dict[str, Any] = field(default_factory=dict)
    ip_address: str = ""
    user_agent: str = ""
    result: str = "success"
    error: str = ""
    correlation_id: str = ""
    tags: List[str] = field(default_factory=list)
    checksum: str = ""
    session_id: str = ""

    def __post_init__(self):
        if not self.checksum:
            self.checksum = self._compute_checksum()

    def _compute_checksum(self) -> str:
        data = f"{self.id}{self.action}{self.actor}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["level"] = self.level.value
        d["category"] = self.category.value
        return d

    @classmethod
    def from_dict(cls, data: Dict) -> "AuditEntry":
        data["level"] = AuditLevel(data["level"])
        data["category"] = AuditCategory(data.get("category", "system"))
        return cls(**data)

    def verify_integrity(self) -> bool:
        return self.checksum == self._compute_checksum()


class AuditQueryBuilder:
    """Fluent query builder for audit logs."""

    def __init__(self, entries: List[AuditEntry]):
        self._entries = entries
        self._filters: List[Callable] = []

    def action(self, action: str) -> "AuditQueryBuilder":
        self._filters.append(lambda e: e.action == action)
        return self

    def actions(self, actions: List[str]) -> "AuditQueryBuilder":
        action_set = set(actions)
        self._filters.append(lambda e: e.action in action_set)
        return self

    def actor(self, actor: str) -> "AuditQueryBuilder":
        self._filters.append(lambda e: e.actor == actor)
        return self

    def actors(self, actors: List[str]) -> "AuditQueryBuilder":
        actor_set = set(actors)
        self._filters.append(lambda e: e.actor in actor_set)
        return self

    def resource(self, resource: str) -> "AuditQueryBuilder":
        self._filters.append(lambda e: e.resource == resource)
        return self

    def level(self, level: AuditLevel) -> "AuditQueryBuilder":
        self._filters.append(lambda e: e.level == level)
        return self

    def min_level(self, level: AuditLevel) -> "AuditQueryBuilder":
        levels = list(AuditLevel)
        min_idx = levels.index(level)
        self._filters.append(lambda e: levels.index(e.level) >= min_idx)
        return self

    def category(self, category: AuditCategory) -> "AuditQueryBuilder":
        self._filters.append(lambda e: e.category == category)
        return self

    def categories(self, categories: List[AuditCategory]) -> "AuditQueryBuilder":
        cat_set = set(categories)
        self._filters.append(lambda e: e.category in cat_set)
        return self

    def result(self, result: str) -> "AuditQueryBuilder":
        self._filters.append(lambda e: e.result == result)
        return self

    def failures_only(self) -> "AuditQueryBuilder":
        self._filters.append(lambda e: e.result != "success")
        return self

    def errors_only(self) -> "AuditQueryBuilder":
        self._filters.append(lambda e: e.level in (AuditLevel.ERROR, AuditLevel.CRITICAL))
        return self

    def after(self, timestamp: float) -> "AuditQueryBuilder":
        self._filters.append(lambda e: e.timestamp >= timestamp)
        return self

    def before(self, timestamp: float) -> "AuditQueryBuilder":
        self._filters.append(lambda e: e.timestamp <= timestamp)
        return self

    def between(self, start: float, end: float) -> "AuditQueryBuilder":
        self._filters.append(lambda e: start <= e.timestamp <= end)
        return self

    def last_hours(self, hours: int) -> "AuditQueryBuilder":
        cutoff = time.time() - (hours * 3600)
        self._filters.append(lambda e: e.timestamp >= cutoff)
        return self

    def last_days(self, days: int) -> "AuditQueryBuilder":
        cutoff = time.time() - (days * 86400)
        self._filters.append(lambda e: e.timestamp >= cutoff)
        return self

    def tag(self, tag: str) -> "AuditQueryBuilder":
        self._filters.append(lambda e: tag in e.tags)
        return self

    def tags(self, tags: List[str]) -> "AuditQueryBuilder":
        tag_set = set(tags)
        self._filters.append(lambda e: bool(set(e.tags) & tag_set))
        return self

    def search(self, query: str) -> "AuditQueryBuilder":
        query_lower = query.lower()
        self._filters.append(lambda e: (
            query_lower in e.action.lower() or
            query_lower in e.resource.lower() or
            query_lower in str(e.details).lower()
        ))
        return self

    def ip(self, ip_address: str) -> "AuditQueryBuilder":
        self._filters.append(lambda e: e.ip_address == ip_address)
        return self

    def execute(self, limit: int = 100, offset: int = 0,
                sort_by: str = "timestamp", reverse: bool = True) -> List[AuditEntry]:
        results = self._entries
        for f in self._filters:
            results = [e for e in results if f(e)]

        if sort_by == "timestamp":
            results.sort(key=lambda e: e.timestamp, reverse=reverse)
        elif sort_by == "action":
            results.sort(key=lambda e: e.action, reverse=reverse)
        elif sort_by == "actor":
            results.sort(key=lambda e: e.actor, reverse=reverse)

        return results[offset:offset + limit]

    def count(self) -> int:
        results = self._entries
        for f in self._filters:
            results = [e for e in results if f(e)]
        return len(results)

    def first(self) -> Optional[AuditEntry]:
        results = self.execute(limit=1)
        return results[0] if results else None

    def to_dicts(self, limit: int = 100) -> List[Dict]:
        return [e.to_dict() for e in self.execute(limit=limit)]

    def to_json(self, limit: int = 100) -> str:
        return json.dumps(self.to_dicts(limit), indent=2, default=str)

    def to_csv(self, limit: int = 100) -> str:
        entries = self.execute(limit=limit)
        if not entries:
            return ""
        output = io.StringIO()
        fields = ["id", "timestamp", "action", "actor", "resource", "level", "result", "error"]
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for e in entries:
            d = e.to_dict()
            writer.writerow({k: d.get(k, "") for k in fields})
        return output.getvalue()

    def group_by(self, field: str) -> Dict[str, List[AuditEntry]]:
        results = self.execute(limit=10000)
        groups: Dict[str, List[AuditEntry]] = {}
        for entry in results:
            key = getattr(entry, field, "unknown")
            if isinstance(key, Enum):
                key = key.value
            groups.setdefault(str(key), []).append(entry)
        return groups

    def aggregate(self) -> Dict:
        results = self.execute(limit=10000)
        return {
            "total": len(results),
            "by_action": len(set(e.action for e in results)),
            "by_actor": len(set(e.actor for e in results)),
            "by_level": {lv.value: sum(1 for e in results if e.level == lv) for lv in AuditLevel},
            "by_result": {
                "success": sum(1 for e in results if e.result == "success"),
                "failure": sum(1 for e in results if e.result != "success"),
            },
            "by_category": {cat.value: sum(1 for e in results if e.category == cat) for cat in AuditCategory},
            "time_range": {
                "earliest": min(e.timestamp for e in results) if results else 0,
                "latest": max(e.timestamp for e in results) if results else 0,
            },
        }


class AuditLog:
    def __init__(self, log_dir: str = "data/audit", max_memory_entries: int = 10000,
                 retention_days: int = 90):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.entries: List[AuditEntry] = []
        self.max_memory = max_memory_entries
        self.retention_days = retention_days
        self._lock = threading.Lock()
        self._listeners: List[Callable] = []
        self._load_recent()

    def _load_recent(self):
        today = datetime.now().strftime("%Y-%m-%d")
        file_path = self.log_dir / f"audit-{today}.jsonl"
        if file_path.exists():
            try:
                with open(file_path) as f:
                    for line in f:
                        if line.strip():
                            try:
                                self.entries.append(AuditEntry.from_dict(json.loads(line)))
                            except Exception:
                                pass
            except Exception:
                pass

    def on_entry(self, callback: Callable):
        self._listeners.append(callback)

    def log(self, action: str, actor: str, resource: str, resource_id: str = "",
            level: AuditLevel = AuditLevel.INFO, details: Dict = None,
            ip_address: str = "", result: str = "success", error: str = "",
            correlation_id: str = "", tags: List[str] = None,
            category: AuditCategory = AuditCategory.SYSTEM,
            session_id: str = "", user_agent: str = "") -> AuditEntry:
        entry = AuditEntry(
            id=str(uuid.uuid4()),
            action=action,
            actor=actor,
            resource=resource,
            resource_id=resource_id or str(uuid.uuid4())[:8],
            level=level,
            timestamp=time.time(),
            category=category,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            result=result,
            error=error,
            correlation_id=correlation_id,
            tags=tags or [],
            session_id=session_id,
        )

        with self._lock:
            self.entries.append(entry)
            if len(self.entries) > self.max_memory:
                self.entries = self.entries[-self.max_memory:]

        self._persist(entry)

        for listener in self._listeners:
            try:
                listener(entry)
            except Exception as e:
                logger.error(f"Audit listener error: {e}")

        return entry

    def _persist(self, entry: AuditEntry):
        try:
            date_str = datetime.fromtimestamp(entry.timestamp).strftime("%Y-%m-%d")
            file_path = self.log_dir / f"audit-{date_str}.jsonl"
            with open(file_path, "a") as f:
                f.write(json.dumps(entry.to_dict()) + "\n")
        except Exception as e:
            logger.error(f"Failed to persist audit entry: {e}")

    def query(self, **kwargs) -> AuditQueryBuilder:
        return AuditQueryBuilder(self.entries)

    def query_action(self, action: str = None, actor: str = None, resource: str = None,
                     level: AuditLevel = None, start: float = None, end: float = None,
                     limit: int = 100) -> List[AuditEntry]:
        q = AuditQueryBuilder(self.entries)
        if action:
            q = q.action(action)
        if actor:
            q = q.actor(actor)
        if resource:
            q = q.resource(resource)
        if level:
            q = q.level(level)
        if start:
            q = q.after(start)
        if end:
            q = q.before(end)
        return q.execute(limit=limit)

    def query_file(self, date: str, action: str = None, actor: str = None) -> List[AuditEntry]:
        file_path = self.log_dir / f"audit-{date}.jsonl"
        results = []
        if not file_path.exists():
            return results
        with open(file_path) as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    entry = AuditEntry.from_dict(data)
                    if action and entry.action != action:
                        continue
                    if actor and entry.actor != actor:
                        continue
                    results.append(entry)
                except Exception:
                    pass
        return results

    def count(self, action: str = None) -> int:
        if action:
            return sum(1 for e in self.entries if e.action == action)
        return len(self.entries)

    def get_stats(self) -> Dict:
        return {
            "total": len(self.entries),
            "by_level": {lv.value: sum(1 for e in self.entries if e.level == lv)
                         for lv in AuditLevel},
            "by_category": {cat.value: sum(1 for e in self.entries if e.category == cat)
                            for cat in AuditCategory},
            "by_result": {
                "success": sum(1 for e in self.entries if e.result == "success"),
                "failure": sum(1 for e in self.entries if e.result != "success"),
            },
            "unique_actors": len(set(e.actor for e in self.entries)),
            "unique_resources": len(set(e.resource for e in self.entries)),
            "unique_ips": len(set(e.ip_address for e in self.entries if e.ip_address)),
            "integrity_verified": all(e.verify_integrity() for e in self.entries),
        }

    def export_json(self, start: float = None, end: float = None) -> str:
        q = AuditQueryBuilder(self.entries)
        if start:
            q = q.after(start)
        if end:
            q = q.before(end)
        return q.to_json(limit=10000)

    def export_csv(self, start: float = None, end: float = None) -> str:
        q = AuditQueryBuilder(self.entries)
        if start:
            q = q.after(start)
        if end:
            q = q.before(end)
        return q.to_csv(limit=10000)

    def cleanup_old(self) -> int:
        cutoff = time.time() - (self.retention_days * 86400)
        old_count = len(self.entries)
        with self._lock:
            self.entries = [e for e in self.entries if e.timestamp >= cutoff]
        removed = old_count - len(self.entries)
        if removed > 0:
            logger.info(f"Cleaned up {removed} audit entries older than {self.retention_days} days")
        return removed

    def verify_integrity(self) -> Dict:
        total = len(self.entries)
        valid = sum(1 for e in self.entries if e.verify_integrity())
        return {
            "total": total,
            "valid": valid,
            "invalid": total - valid,
            "integrity_rate": valid / total if total > 0 else 1.0,
        }

    def get_actor_timeline(self, actor: str, hours: int = 24) -> List[Dict]:
        cutoff = time.time() - (hours * 3600)
        entries = [e for e in self.entries if e.actor == actor and e.timestamp >= cutoff]
        return [{"time": e.timestamp, "action": e.action, "resource": e.resource}
                for e in sorted(entries, key=lambda e: e.timestamp)]

    def get_failed_actions(self, hours: int = 24) -> List[AuditEntry]:
        return AuditQueryBuilder(self.entries).failures_only().last_hours(hours).execute()

    def get_security_events(self, hours: int = 24) -> List[AuditEntry]:
        return (AuditQueryBuilder(self.entries)
                .categories([AuditCategory.SECURITY, AuditCategory.AUTH])
                .last_hours(hours)
                .execute())
