from __future__ import annotations

from .adapters import AWSRDSAdapter, AzurePGAdapter, GCPAdapter
from .models import CloudAdapter, CloudProvider, ConnectionInfo, QueryResult


class CloudProxy:
    def __init__(self) -> None:
        self._adapters: dict[CloudProvider, CloudAdapter] = {
            CloudProvider.AWS: AWSRDSAdapter(),
            CloudProvider.AZURE: AzurePGAdapter(),
            CloudProvider.GCP: GCPAdapter(),
        }
        self._active_provider: CloudProvider | None = None
        self._query_count = 0

    @property
    def active_provider(self) -> CloudProvider | None:
        return self._active_provider

    @property
    def query_count(self) -> int:
        return self._query_count

    def register_adapter(self, adapter: CloudAdapter) -> None:
        self._adapters[adapter.provider] = adapter

    def get_adapter(self, provider: CloudProvider) -> CloudAdapter:
        if provider not in self._adapters:
            msg = f"No adapter for provider {provider.value}"
            raise KeyError(msg)
        return self._adapters[provider]

    def connect(self, info: ConnectionInfo) -> bool:
        adapter = self.get_adapter(info.provider)
        result = adapter.connect(info)
        if result:
            self._active_provider = info.provider
        return result

    def query(self, sql: str) -> QueryResult:
        if self._active_provider is None:
            msg = "No active connection"
            raise RuntimeError(msg)
        adapter = self._adapters[self._active_provider]
        result = adapter.query(sql)
        self._query_count += 1
        return result

    def disconnect(self) -> bool:
        if self._active_provider is None:
            return False
        adapter = self._adapters[self._active_provider]
        result = adapter.disconnect()
        if result:
            self._active_provider = None
        return result

    def list_providers(self) -> list[CloudProvider]:
        return list(self._adapters.keys())
