import pytest
from pg_cloudproxy.adapters import AWSRDSAdapter, AzurePGAdapter, GCPAdapter
from pg_cloudproxy.models import CloudProvider, ConnectionInfo
from pg_cloudproxy.proxy import CloudProxy


def _info(provider: CloudProvider) -> ConnectionInfo:
    return ConnectionInfo(
        host="localhost", port=5432, database="db", username="u", provider=provider
    )


def test_proxy_connects_aws() -> None:
    proxy = CloudProxy()
    assert proxy.connect(_info(CloudProvider.AWS))
    assert proxy.active_provider == CloudProvider.AWS


def test_proxy_query() -> None:
    proxy = CloudProxy()
    proxy.connect(_info(CloudProvider.GCP))
    result = proxy.query("SELECT 1")
    assert result.provider == CloudProvider.GCP
    assert proxy.query_count == 1


def test_proxy_disconnect() -> None:
    proxy = CloudProxy()
    proxy.connect(_info(CloudProvider.AZURE))
    assert proxy.disconnect()
    assert proxy.active_provider is None


def test_proxy_query_without_connection_raises() -> None:
    proxy = CloudProxy()
    with pytest.raises(RuntimeError):
        proxy.query("SELECT 1")


def test_proxy_list_providers() -> None:
    proxy = CloudProxy()
    providers = proxy.list_providers()
    assert CloudProvider.AWS in providers
    assert CloudProvider.AZURE in providers
    assert CloudProvider.GCP in providers


def test_aws_adapter_provider() -> None:
    a = AWSRDSAdapter()
    assert a.provider == CloudProvider.AWS


def test_azure_adapter_provider() -> None:
    a = AzurePGAdapter()
    assert a.provider == CloudProvider.AZURE
