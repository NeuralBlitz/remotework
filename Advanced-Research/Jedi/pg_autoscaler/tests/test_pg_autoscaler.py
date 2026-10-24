from pg_autoscaler.models import ClusterMetrics, ClusterStatus
from pg_autoscaler.observers import ScaleDownObserver, ScaleUpObserver
from pg_autoscaler.subject import ClusterMetricsSubject


def test_subject_attaches_observer() -> None:
    subject = ClusterMetricsSubject()
    obs = ScaleUpObserver()
    subject.attach(obs)
    assert subject.observer_count == 1


def test_subject_detaches_observer() -> None:
    subject = ClusterMetricsSubject()
    obs = ScaleUpObserver()
    subject.attach(obs)
    subject.detach(obs)
    assert subject.observer_count == 0


def test_scale_up_on_high_cpu() -> None:
    subject = ClusterMetricsSubject()
    obs = ScaleUpObserver(threshold_cpu=80.0)
    subject.attach(obs)
    m = ClusterMetrics(cpu_percent=95.0, replica_count=2)
    subject.update_metrics(m)
    assert len(obs.events) == 1
    assert obs.events[0].new_count == 3


def test_scale_down_on_low_load() -> None:
    subject = ClusterMetricsSubject()
    obs = ScaleDownObserver(threshold_cpu=30.0)
    subject.attach(obs)
    m = ClusterMetrics(cpu_percent=10.0, replica_count=3, max_connections=100, connections=10)
    subject.update_metrics(m)
    assert len(obs.events) == 1
    assert obs.events[0].new_count == 2


def test_scale_down_respects_min_replicas() -> None:
    obs = ScaleDownObserver()
    obs.set_min_replicas(2)
    m = ClusterMetrics(cpu_percent=10.0, replica_count=2, max_connections=100, connections=5)
    obs.update(m)
    assert len(obs.events) == 0


def test_cluster_status_overloaded() -> None:
    m = ClusterMetrics(cpu_percent=95.0)
    assert m.status == ClusterStatus.OVERLOADED


def test_cluster_status_healthy() -> None:
    m = ClusterMetrics(cpu_percent=30.0, max_connections=100, connections=10)
    assert m.status == ClusterStatus.HEALTHY
