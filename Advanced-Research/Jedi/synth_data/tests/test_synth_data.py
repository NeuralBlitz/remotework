import pytest

from synth_data.generator import SyntheticDataGenerator
from synth_data.memento import GeneratorMemento, PrivacyCaretaker
from synth_data.models import PrivacyMetrics, SyntheticConfig


def test_generate_data():
    config = SyntheticConfig(num_rows=10, num_columns=5)
    gen = SyntheticDataGenerator(config)
    data = gen.generate()
    assert len(data) == 10
    assert len(data[0]) == 5


def test_save_and_restore():
    config = SyntheticConfig(num_rows=5, num_columns=3)
    gen = SyntheticDataGenerator(config)
    gen.generate()
    memento = gen.save_state()
    gen.generate()
    gen.restore_state(memento)
    assert gen.iteration == memento.iteration


def test_undo_redo():
    config = SyntheticConfig(num_rows=5, num_columns=3)
    gen = SyntheticDataGenerator(config)
    gen.save_state()
    gen.generate()
    gen.save_state()
    gen.generate()
    assert gen.undo()
    assert gen.redo()


def test_privacy_budget():
    metrics = PrivacyMetrics(epsilon_used=0.5)
    assert metrics.budget_remaining(1.0) == 0.5
    assert metrics.budget_remaining(0.3) == 0.0


def test_is_private():
    assert PrivacyMetrics(uniqueness_ratio=0.05).is_private()
    assert not PrivacyMetrics(uniqueness_ratio=0.5).is_private()


def test_invalid_config():
    config = SyntheticConfig(num_rows=-1)
    assert not config.validate()


def test_caretaker_history():
    ct = PrivacyCaretaker()
    m1 = GeneratorMemento(SyntheticConfig(), PrivacyMetrics(), 1, "abc")
    m2 = GeneratorMemento(SyntheticConfig(), PrivacyMetrics(), 2, "def")
    ct.save(m1)
    ct.save(m2)
    assert ct.history_size() == 2
    assert ct.can_undo()
    assert not ct.can_redo()
