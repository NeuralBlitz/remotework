from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class DeviceStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"


@dataclass
class DeviceState:
    device_id: str
    status: DeviceStatus
    firmware_version: str
    telemetry: dict[str, Any] = field(default_factory=dict)
    config: dict[str, Any] = field(default_factory=dict)
    last_seen: datetime = field(default_factory=datetime.utcnow)
    error_count: int = 0

    def snapshot(self) -> DeviceMemento:
        return DeviceMemento(
            device_id=self.device_id,
            status=self.status,
            firmware_version=self.firmware_version,
            telemetry=dict(self.telemetry),
            config=dict(self.config),
            last_seen=self.last_seen,
            error_count=self.error_count,
            timestamp=datetime.utcnow(),
        )


@dataclass(frozen=True)
class DeviceMemento:
    device_id: str
    status: DeviceStatus
    firmware_version: str
    telemetry: dict[str, Any]
    config: dict[str, Any]
    last_seen: datetime
    error_count: int
    timestamp: datetime

    def restore(self) -> DeviceState:
        return DeviceState(
            device_id=self.device_id,
            status=self.status,
            firmware_version=self.firmware_version,
            telemetry=dict(self.telemetry),
            config=dict(self.config),
            last_seen=self.last_seen,
            error_count=self.error_count,
        )
