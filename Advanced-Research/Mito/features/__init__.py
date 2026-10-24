"""
Mito Feature Flags
Feature flag management with percentage rollout, user targeting, segments
"""

import json
import hashlib
import logging
import time
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

logger = logging.getLogger("mito.features")


class FlagType(Enum):
    BOOLEAN = "boolean"
    STRING = "string"
    NUMBER = "number"
    JSON = "json"


@dataclass
class FeatureFlag:
    name: str
    flag_type: FlagType = FlagType.BOOLEAN
    enabled: bool = True
    default_value: Any = None
    rollout_percentage: float = 100.0
    allowed_users: Set[str] = field(default_factory=set)
    blocked_users: Set[str] = field(default_factory=set)
    segments: Dict[str, Any] = field(default_factory=dict)
    variants: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    tags: List[str] = field(default_factory=list)
    expires_at: float = 0


class FeatureFlagManager:
    def __init__(self, flags_file: str = "data/flags.json"):
        self.flags_file = Path(flags_file)
        self.flags: Dict[str, FeatureFlag] = {}
        self._load()

    def _load(self):
        if self.flags_file.exists():
            try:
                with open(self.flags_file) as f:
                    data = json.load(f)
                for name, fd in data.items():
                    self.flags[name] = FeatureFlag(
                        name=name,
                        flag_type=FlagType(fd.get("flag_type", "boolean")),
                        enabled=fd.get("enabled", True),
                        default_value=fd.get("default_value"),
                        rollout_percentage=fd.get("rollout_percentage", 100),
                        allowed_users=set(fd.get("allowed_users", [])),
                        blocked_users=set(fd.get("blocked_users", [])),
                        segments=fd.get("segments", {}),
                        variants=fd.get("variants", {}),
                        description=fd.get("description", ""),
                        created_at=fd.get("created_at", time.time()),
                        updated_at=fd.get("updated_at", time.time()),
                        tags=fd.get("tags", []),
                        expires_at=fd.get("expires_at", 0),
                    )
            except Exception as e:
                logger.error(f"Failed to load flags: {e}")

    def _save(self):
        self.flags_file.parent.mkdir(parents=True, exist_ok=True)
        data = {}
        for name, flag in self.flags.items():
            data[name] = {
                "flag_type": flag.flag_type.value,
                "enabled": flag.enabled,
                "default_value": flag.default_value,
                "rollout_percentage": flag.rollout_percentage,
                "allowed_users": list(flag.allowed_users),
                "blocked_users": list(flag.blocked_users),
                "segments": flag.segments,
                "variants": flag.variants,
                "description": flag.description,
                "created_at": flag.created_at,
                "updated_at": flag.updated_at,
                "tags": flag.tags,
                "expires_at": flag.expires_at,
            }
        with open(self.flags_file, "w") as f:
            json.dump(data, f, indent=2)

    def create(self, name: str, flag_type: FlagType = FlagType.BOOLEAN,
               enabled: bool = True, default_value: Any = None, **kwargs) -> FeatureFlag:
        flag = FeatureFlag(
            name=name, flag_type=flag_type, enabled=enabled,
            default_value=default_value, **kwargs,
        )
        self.flags[name] = flag
        self._save()
        logger.info(f"Created feature flag '{name}'")
        return flag

    def update(self, name: str, **kwargs) -> Optional[FeatureFlag]:
        if name not in self.flags:
            return None
        flag = self.flags[name]
        for key, value in kwargs.items():
            if hasattr(flag, key):
                setattr(flag, key, value)
        flag.updated_at = time.time()
        self._save()
        return flag

    def delete(self, name: str) -> bool:
        if name in self.flags:
            del self.flags[name]
            self._save()
            return True
        return False

    def is_enabled(self, flag_name: str, user_id: str = None, context: Dict = None) -> bool:
        flag = self.flags.get(flag_name)
        if not flag:
            return False

        if not flag.enabled:
            return False

        if flag.expires_at and time.time() > flag.expires_at:
            return False

        if user_id:
            if user_id in flag.blocked_users:
                return False
            if flag.allowed_users and user_id not in flag.allowed_users:
                return False

            if flag.rollout_percentage < 100:
                hash_val = int(hashlib.md5(f"{flag_name}:{user_id}".encode()).hexdigest(), 16)
                user_pct = (hash_val % 10000) / 100.0
                if user_pct > flag.rollout_percentage:
                    return False

        if context and flag.segments:
            for key, expected in flag.segments.items():
                if context.get(key) != expected:
                    return False

        return True

    def get_value(self, flag_name: str, user_id: str = None, context: Dict = None) -> Any:
        flag = self.flags.get(flag_name)
        if not flag:
            return None

        if not self.is_enabled(flag_name, user_id, context):
            return flag.default_value

        if flag.variants and user_id:
            hash_val = int(hashlib.md5(f"{flag_name}:variant:{user_id}".encode()).hexdigest(), 16)
            total = sum(flag.variants.values())
            cumulative = 0
            target = hash_val % total
            for variant_name, weight in flag.variants.items():
                cumulative += weight
                if target < cumulative:
                    return variant_name

        return flag.default_value if flag.default_value is not None else flag.enabled

    def list_flags(self, tags: List[str] = None) -> List[FeatureFlag]:
        flags = list(self.flags.values())
        if tags:
            flags = [f for f in flags if set(tags) & set(f.tags)]
        return flags

    def get_stats(self) -> Dict:
        return {
            "total": len(self.flags),
            "enabled": sum(1 for f in self.flags.values() if f.enabled),
            "disabled": sum(1 for f in self.flags.values() if not f.enabled),
            "types": {t.value: sum(1 for f in self.flags.values() if f.flag_type == t)
                      for t in FlagType},
        }
