from src.climate_risk.models import BaseModel, Config


class TestConfig:
    def test_config_creation(self) -> None:
        config = Config(name="test", value=1.0)
        assert config.name == "test"
        assert config.value == 1.0

    def test_config_str(self) -> None:
        config = Config(name="test", value=2.5)
        assert str(config) == "Config(name='test', value=2.5)"


class TestBaseModel:
    def test_model_protocol_exists(self) -> None:
        assert BaseModel is not None

    def test_model_has_predict_method(self) -> None:
        assert hasattr(BaseModel, "predict")

    def test_model_has_train_method(self) -> None:
        assert hasattr(BaseModel, "train")


class TestClimate_riskModule:
    def test_module_import(self) -> None:
        from src import climate_risk
        assert climate_risk is not None

    def test_version_exists(self) -> None:
        from src.climate_risk import __version__
        assert __version__ == "0.1.0"

    def test_config_in_module(self) -> None:
        from src.climate_risk.models import Config
        assert Config is not None

    def test_description_in_init(self) -> None:
        from src.climate_risk import __doc__
        assert __doc__ is not None
        assert len(__doc__) > 0
