from zero_trust.models import BaseModel, Prediction, create_model, predict


class TestZerotrustModels:
    def test_create_model(self):
        model = create_model("Test Model", "1.0.0")
        assert isinstance(model, BaseModel)
        assert model.name == "Test Model"
        assert model.version == "1.0.0"
        assert model.enabled is True

    def test_create_model_default_version(self):
        model = create_model("Test Model")
        assert model.version == "0.1.0"

    def test_model_id_is_sanitized(self):
        model = create_model("Test Model Name")
        assert " " not in model.id
        assert model.id == "test_model_name"

    def test_predict_returns_prediction(self):
        model = create_model("Test")
        result = predict(model, {"key": "value"})
        assert isinstance(result, Prediction)
        assert result.model_id == model.id

    def test_predict_has_confidence(self):
        model = create_model("Test")
        result = predict(model, {})
        assert 0.0 <= result.confidence <= 1.0

    def test_predict_stores_input_data(self):
        model = create_model("Test")
        input_data = {"feature1": 1, "feature2": 2}
        result = predict(model, input_data)
        assert result.input_data == input_data

    def test_base_model_defaults(self):
        model = create_model("Test")
        assert model.enabled is True
