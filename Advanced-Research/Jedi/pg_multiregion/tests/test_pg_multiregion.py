import pytest
from pg_multiregion.mediator import RegionMediator
from pg_multiregion.models import RegionNode, SyncStatus
from pg_multiregion.sync import RegionSyncer


def _make_mediator() -> RegionMediator:
    m = RegionMediator()
    m.register_region(RegionNode("us-east", "10.0.0.1:5432"))
    m.register_region(RegionNode("eu-west", "10.0.0.2:5432"))
    return m


def test_register_and_list_regions() -> None:
    m = _make_mediator()
    assert len(m.list_regions()) == 2


def test_unregister_region() -> None:
    m = _make_mediator()
    assert m.unregister_region("us-east")
    assert len(m.list_regions()) == 1


def test_route_sync() -> None:
    m = _make_mediator()
    event = m.route_sync("us-east", "eu-west", 100)
    assert event.status == SyncStatus.SYNCED
    assert event.records_synced == 100


def test_route_sync_unknown_source_raises() -> None:
    m = _make_mediator()
    with pytest.raises(KeyError):
        m.route_sync("nope", "eu-west", 10)


def test_syncer_queues_and_flushes() -> None:
    m = _make_mediator()
    syncer = RegionSyncer("us-east", m)
    syncer.queue_change("k1", "v1")
    syncer.queue_change("k2", "v2")
    assert syncer.pending_count == 2
    events = syncer.flush("eu-west")
    assert len(events) == 1
    assert syncer.synced_count == 2
    assert syncer.pending_count == 0


def test_syncer_sync_to() -> None:
    m = _make_mediator()
    syncer = RegionSyncer("us-east", m)
    event = syncer.sync_to("eu-west", 50)
    assert event.records_synced == 50
    assert syncer.synced_count == 50


def test_mediator_get_events() -> None:
    m = _make_mediator()
    m.route_sync("us-east", "eu-west", 10)
    assert len(m.get_events()) == 1
