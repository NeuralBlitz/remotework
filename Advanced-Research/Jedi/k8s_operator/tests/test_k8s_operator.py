import pytest
from k8s_operator.models import PGCluster, PGClusterSpec, PGClusterStatus, ClusterPhase
from k8s_operator.operator import PGOperator, ReconcileResult
from k8s_operator.controller import ResourceController, ResourceEvent


def test_pgcluster_creation() -> None:
    cluster = PGCluster(name="test-pg", namespace="default")
    assert cluster.name == "test-pg"
    assert cluster.namespace == "default"
    assert cluster.spec.replicas == 3


def test_pgcluster_spec_defaults() -> None:
    spec = PGClusterSpec()
    assert spec.version == "16.2"
    assert spec.storage_size_gb == 100
    assert spec.max_connections == 200
    assert spec.enable_ssl is True


def test_pgcluster_is_ready() -> None:
    cluster = PGCluster(name="ready-pg", namespace="prod")
    cluster.status.phase = ClusterPhase.RUNNING
    cluster.status.ready_replicas = 3
    assert cluster.is_ready is True


def test_pgcluster_not_ready() -> None:
    cluster = PGCluster(name="pending-pg", namespace="prod")
    assert cluster.is_ready is False


def test_pgcluster_add_label() -> None:
    cluster = PGCluster(name="labeled", namespace="default")
    cluster.add_label("env", "prod")
    assert cluster.labels["env"] == "prod"


def test_operator_register() -> None:
    op = PGOperator()
    cluster = PGCluster(name="c1", namespace="default")
    op.register_cluster(cluster)
    assert op.cluster_count == 1


def test_operator_reconcile() -> None:
    op = PGOperator()
    cluster = PGCluster(name="c2", namespace="default")
    op.register_cluster(cluster)
    result = op.reconcile("c2")
    assert result.changed is True
    assert "initialized_cluster" in result.actions


def test_operator_reconcile_not_found() -> None:
    op = PGOperator()
    result = op.reconcile("nonexistent")
    assert result.error == "Cluster not found"


def test_operator_reconcile_all() -> None:
    op = PGOperator()
    for i in range(3):
        op.register_cluster(PGCluster(name=f"cluster-{i}", namespace="default"))
    results = op.reconcile_all()
    assert len(results) == 3


def test_controller_handle_add() -> None:
    op = PGOperator()
    ctrl = ResourceController(op)
    event = ResourceEvent(
        event_type="ADD",
        resource_name="new-pg",
        namespace="default",
        payload={"spec": {"replicas": 5}},
    )
    assert ctrl.handle_event(event) is True
    assert op.cluster_count == 1


def test_controller_handle_delete() -> None:
    op = PGOperator()
    cluster = PGCluster(name="del-pg", namespace="default")
    op.register_cluster(cluster)
    ctrl = ResourceController(op)
    event = ResourceEvent(event_type="DELETE", resource_name="del-pg", namespace="default")
    ctrl.handle_event(event)
    assert op.cluster_count == 0


def test_controller_lifecycle() -> None:
    op = PGOperator()
    ctrl = ResourceController(op)
    assert ctrl.is_running is False
    ctrl.start()
    assert ctrl.is_running is True
    ctrl.stop()
    assert ctrl.is_running is False


def test_controller_event_count() -> None:
    op = PGOperator()
    ctrl = ResourceController(op)
    for i in range(5):
        ctrl.handle_event(ResourceEvent(event_type="ADD", resource_name=f"pg-{i}", namespace="ns"))
    assert ctrl.event_count == 5
