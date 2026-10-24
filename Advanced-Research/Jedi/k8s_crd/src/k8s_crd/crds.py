from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CRDVersion(str, Enum):
    V1 = "v1"
    V1BETA1 = "v1beta1"


@dataclass
class PGDatabaseCRD:
    name: str
    namespace: str
    database_name: str
    owner: str
    encoding: str = "UTF8"
    schema_version: str = "1.0"
    extensions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "apiVersion": "postgresql.io/v1",
            "kind": "PGDatabase",
            "metadata": {"name": self.name, "namespace": self.namespace},
            "spec": {
                "databaseName": self.database_name,
                "owner": self.owner,
                "encoding": self.encoding,
                "schemaVersion": self.schema_version,
                "extensions": self.extensions,
            },
        }


@dataclass
class PGBackupCRD:
    name: str
    namespace: str
    source_cluster: str
    backup_type: str = "full"
    retention_days: int = 30
    schedule: str = ""
    compress: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "apiVersion": "postgresql.io/v1",
            "kind": "PGBackup",
            "metadata": {"name": self.name, "namespace": self.namespace},
            "spec": {
                "sourceCluster": self.source_cluster,
                "backupType": self.backup_type,
                "retentionDays": self.retention_days,
                "schedule": self.schedule,
                "compress": self.compress,
            },
        }


@dataclass
class PGUserCRD:
    name: str
    namespace: str
    username: str
    roles: list[str] = field(default_factory=list)
    databases: list[str] = field(default_factory=list)
    password_secret: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "apiVersion": "postgresql.io/v1",
            "kind": "PGUser",
            "metadata": {"name": self.name, "namespace": self.namespace},
            "spec": {
                "username": self.username,
                "roles": self.roles,
                "databases": self.databases,
                "passwordSecret": self.password_secret,
            },
        }
