"""
Mito Session Manager
Session storage with TTL, state management, and multi-backend support
"""

import json
import time
import uuid
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
import threading

logger = logging.getLogger("mito.sessions")


@dataclass
class Session:
    id: str
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    expires_at: float = 0
    user_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        if self.expires_at <= 0:
            return False
        return time.time() > self.expires_at

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        self.data[key] = value
        self.updated_at = time.time()

    def delete(self, key: str) -> bool:
        if key in self.data:
            del self.data[key]
            self.updated_at = time.time()
            return True
        return False

    def clear(self):
        self.data.clear()
        self.updated_at = time.time()


class SessionManager:
    def __init__(self, ttl: int = 3600, persist_file: str = "data/sessions.json"):
        self.ttl = ttl
        self.persist_file = Path(persist_file)
        self.sessions: Dict[str, Session] = {}
        self._lock = threading.Lock()
        self._load()

    def _load(self):
        if self.persist_file.exists():
            try:
                with open(self.persist_file) as f:
                    data = json.load(f)
                for sid, sd in data.items():
                    session = Session(
                        id=sid,
                        data=sd.get("data", {}),
                        created_at=sd.get("created_at", time.time()),
                        updated_at=sd.get("updated_at", time.time()),
                        expires_at=sd.get("expires_at", 0),
                        user_id=sd.get("user_id", ""),
                        metadata=sd.get("metadata", {}),
                    )
                    if not session.is_expired():
                        self.sessions[sid] = session
            except Exception as e:
                logger.error(f"Failed to load sessions: {e}")

    def _save(self):
        self.persist_file.parent.mkdir(parents=True, exist_ok=True)
        data = {}
        for sid, session in self.sessions.items():
            data[sid] = {
                "data": session.data,
                "created_at": session.created_at,
                "updated_at": session.updated_at,
                "expires_at": session.expires_at,
                "user_id": session.user_id,
                "metadata": session.metadata,
            }
        with open(self.persist_file, "w") as f:
            json.dump(data, f)

    def create(self, user_id: str = "", ttl: int = 0, metadata: Dict = None) -> Session:
        session_id = str(uuid.uuid4())
        expires_at = time.time() + (ttl or self.ttl) if (ttl or self.ttl) > 0 else 0
        session = Session(
            id=session_id,
            user_id=user_id,
            expires_at=expires_at,
            metadata=metadata or {},
        )
        with self._lock:
            self.sessions[session_id] = session
            self._save()
        return session

    def get(self, session_id: str) -> Optional[Session]:
        with self._lock:
            session = self.sessions.get(session_id)
            if session and session.is_expired():
                del self.sessions[session_id]
                self._save()
                return None
            return session

    def update(self, session_id: str, data: Dict[str, Any]) -> Optional[Session]:
        with self._lock:
            session = self.sessions.get(session_id)
            if not session or session.is_expired():
                return None
            session.data.update(data)
            session.updated_at = time.time()
            self._save()
            return session

    def delete(self, session_id: str) -> bool:
        with self._lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                self._save()
                return True
            return False

    def touch(self, session_id: str, ttl: int = 0) -> bool:
        with self._lock:
            session = self.sessions.get(session_id)
            if not session:
                return False
            session.updated_at = time.time()
            if ttl > 0:
                session.expires_at = time.time() + ttl
            self._save()
            return True

    def list_user_sessions(self, user_id: str) -> List[Session]:
        with self._lock:
            return [s for s in self.sessions.values() if s.user_id == user_id and not s.is_expired()]

    def cleanup(self) -> int:
        with self._lock:
            expired = [sid for sid, s in self.sessions.items() if s.is_expired()]
            for sid in expired:
                del self.sessions[sid]
            if expired:
                self._save()
            return len(expired)

    def count(self) -> int:
        return len(self.sessions)

    def get_all(self) -> List[Session]:
        return list(self.sessions.values())
