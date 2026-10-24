import pytest

from he_inference.models import EncryptedTensor, HEConfig, HEScheme
from he_inference.proxy import CKKSProxy, HEProxy


def test_encrypt_basic():
    proxy = HEProxy()
    config = HEConfig()
    tensor = proxy.encrypt([1.0, 2.0, 3.0], config)
    assert tensor.is_encrypted
    assert tensor.shape == (3,)
    assert tensor.is_valid()


def test_decrypt_roundtrip():
    proxy = HEProxy()
    config = HEConfig()
    tensor = proxy.encrypt([1.0, 2.0], config)
    result = proxy.decrypt(tensor, config)
    assert len(result) == 2


def test_evaluate_square():
    proxy = HEProxy()
    config = HEConfig()
    tensor = proxy.encrypt([1.0], config)
    squared = proxy.evaluate(tensor, "square")
    assert squared.scale == tensor.scale * 2


def test_evaluate_caching():
    proxy = HEProxy()
    config = HEConfig()
    tensor = proxy.encrypt([1.0], config)
    r1 = proxy.evaluate(tensor, "relu")
    r2 = proxy.evaluate(tensor, "relu")
    assert r1 is r2


def test_invalid_config():
    proxy = HEProxy()
    config = HEConfig(poly_modulus_degree=1234)
    with pytest.raises(ValueError, match="Invalid"):
        proxy.encrypt([1.0], config)


def test_ckks_proxy_encrypt():
    proxy = CKKSProxy()
    config = HEConfig()
    tensor = proxy.encrypt([5.0, 10.0], config)
    assert config.scheme == HEScheme.CKKS
    assert proxy.rescale_count == 1


def test_ckks_rescale():
    proxy = CKKSProxy()
    tensor = EncryptedTensor(b"ct", (2,), 1024.0)
    rescaled = proxy.rescale(tensor)
    assert rescaled.scale == 512.0
    assert proxy.rescale_count == 1


def test_call_count():
    proxy = HEProxy()
    config = HEConfig()
    proxy.encrypt([1.0], config)
    proxy.encrypt([2.0], config)
    assert proxy.call_count == 2


def test_invalid_tensor():
    proxy = HEProxy()
    tensor = EncryptedTensor(b"", ())
    with pytest.raises(ValueError, match="Invalid"):
        proxy.decrypt(tensor, HEConfig())


def test_tensor_size():
    tensor = EncryptedTensor(b"x", (2, 3, 4), 1.0)
    assert tensor.size() == 24
