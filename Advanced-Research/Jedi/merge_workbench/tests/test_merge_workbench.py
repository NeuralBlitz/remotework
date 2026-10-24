from merge_workbench.models import MergeConfig, MergeResult, MergeStrategy
from merge_workbench.template import SlerpMerger, TiesMerger


def _models() -> tuple[dict[str, list[float]], dict[str, list[float]]]:
    return ({"layer1": [1.0, 2.0, 3.0]}, {"layer1": [4.0, 5.0, 6.0]})


def test_slerp_merge_averages() -> None:
    cfg = MergeConfig(MergeStrategy.SLERP, alpha=0.5)
    merger = SlerpMerger(cfg)
    a, b = _models()
    result = merger.run(a, b)
    assert result.success
    assert result.merged_params["layer1"] == [2.5, 3.5, 4.5]


def test_slerp_alpha_zero_uses_model_a() -> None:
    cfg = MergeConfig(MergeStrategy.SLERP, alpha=0.0)
    merger = SlerpMerger(cfg)
    a, b = _models()
    result = merger.run(a, b)
    assert result.merged_params["layer1"] == [1.0, 2.0, 3.0]


def test_ties_merge_sparsifies() -> None:
    cfg = MergeConfig(MergeStrategy.TIES, alpha=0.5, sparsity=0.5)
    merger = TiesMerger(cfg)
    a = {"l": [10.0, 0.01, 5.0, 0.005]}
    b = {"l": [8.0, 0.02, 6.0, 0.001]}
    result = merger.run(a, b)
    assert result.param_count > 0


def test_merge_config_validate() -> None:
    cfg = MergeConfig(MergeStrategy.SLERP, alpha=0.5)
    assert cfg.validate()
    bad = MergeConfig(MergeStrategy.SLERP, alpha=1.5)
    assert not bad.validate()


def test_merge_result_param_count() -> None:
    result = MergeResult(
        config=MergeConfig(MergeStrategy.SLERP), merged_params={"a": [1, 2], "b": [3]}
    )
    assert result.param_count == 3


def test_slerp_only_model_a_keys() -> None:
    cfg = MergeConfig(MergeStrategy.SLERP, alpha=0.5)
    merger = SlerpMerger(cfg)
    a = {"only_a": [1.0, 2.0]}
    b = {"other": [3.0]}
    result = merger.run(a, b)
    assert result.merged_params["only_a"] == [1.0, 2.0]


def test_elapsed_ms_non_negative() -> None:
    cfg = MergeConfig(MergeStrategy.SLERP)
    merger = SlerpMerger(cfg)
    result = merger.run(*_models())
    assert result.elapsed_ms >= 0


def test_ties_alpha_extremes() -> None:
    cfg = MergeConfig(MergeStrategy.TIES, alpha=1.0, sparsity=0.0)
    merger = TiesMerger(cfg)
    a = {"l": [1.0, 2.0]}
    b = {"l": [3.0, 4.0]}
    result = merger.run(a, b)
    assert result.success
