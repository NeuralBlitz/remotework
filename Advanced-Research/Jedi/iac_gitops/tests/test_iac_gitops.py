import pytest
from iac_gitops.models import GitOpsConfig, DeploymentState, DeploymentPhase
from iac_gitops.pipeline import GitOpsPipeline, PipelineStatus
from iac_gitops.reconciler import GitOpsReconciler


def test_gitops_config_creation() -> None:
    config = GitOpsConfig(repo_url="https://github.com/org/infra")
    assert config.branch == "main"
    assert config.auto_sync is True


def test_gitops_config_full_path() -> None:
    config = GitOpsConfig(repo_url="https://github.com/org/gitops", branch="prod", path="apps/")
    assert "prod" in config.full_path


def test_deployment_state_health() -> None:
    state = DeploymentState(app_name="myapp", resources_count=10, healthy_count=8)
    assert state.health_ratio == 0.8


def test_deployment_state_mark_synced() -> None:
    state = DeploymentState(app_name="app")
    state.mark_synced("abc123")
    assert state.current_revision == "abc123"
    assert state.phase == DeploymentPhase.DEPLOYED


def test_pipeline_register() -> None:
    config = GitOpsConfig(repo_url="https://repo")
    pipeline = GitOpsPipeline(config)
    pipeline.register_app("app1", "v1.0")
    assert pipeline.deployment_count == 1


def test_pipeline_sync() -> None:
    config = GitOpsConfig(repo_url="https://repo")
    pipeline = GitOpsPipeline(config)
    pipeline.register_app("app1", "v1.0")
    result = pipeline.run_sync()
    assert result["app1"].synced is True
    assert pipeline.status == PipelineStatus.COMPLETED


def test_pipeline_rollback() -> None:
    config = GitOpsConfig(repo_url="https://repo")
    pipeline = GitOpsPipeline(config)
    pipeline.register_app("app1", "v2.0")
    pipeline.run_sync()
    assert pipeline.rollback("app1", "v1.0") is True


def test_pipeline_rollback_not_found() -> None:
    config = GitOpsConfig(repo_url="https://repo")
    pipeline = GitOpsPipeline(config)
    assert pipeline.rollback("nonexistent", "v1.0") is False


def test_reconciler_set_desired() -> None:
    config = GitOpsConfig(repo_url="https://repo")
    pipeline = GitOpsPipeline(config)
    pipeline.register_app("app1", "v1.0")
    recon = GitOpsReconciler(pipeline)
    recon.set_desired_state("app1", "v2.0")
    assert recon.desired_state_count == 1


def test_reconciler_reconcile() -> None:
    config = GitOpsConfig(repo_url="https://repo")
    pipeline = GitOpsPipeline(config)
    pipeline.register_app("app1", "v1.0")
    recon = GitOpsReconciler(pipeline)
    recon.set_desired_state("app1", "v2.0")
    result = recon.reconcile("app1")
    assert result.success is True
    assert result.action == "sync"


def test_reconciler_reconcile_all() -> None:
    config = GitOpsConfig(repo_url="https://repo")
    pipeline = GitOpsPipeline(config)
    recon = GitOpsReconciler(pipeline)
    for i in range(3):
        pipeline.register_app(f"app-{i}", "v1.0")
        recon.set_desired_state(f"app-{i}", "v2.0")
    results = recon.reconcile_all()
    assert len(results) == 3


def test_pipeline_sync_count() -> None:
    config = GitOpsConfig(repo_url="https://repo")
    pipeline = GitOpsPipeline(config)
    pipeline.run_sync()
    pipeline.run_sync()
    assert pipeline.sync_count == 2
