"""Tests for secret_vault."""
from __future__ import annotations

from src.secret_vault import retrieve_secret, store_secret


def test_store_secret():
    secret = store_secret("api_key", "secret123")
    assert secret.name == "api_key"
    assert secret.encrypted_value == "secret123"

def test_retrieve_secret():
    secret = store_secret("password", "mypassword")
    result = retrieve_secret(secret)
    assert result == "decrypted"

def test_store_multiple_secrets():
    s1 = store_secret("key1", "val1")
    s2 = store_secret("key2", "val2")
    assert s1.name != s2.name

def test_retrieve_decrypt_method():
    secret = store_secret("test", "value")
    decrypted = secret.decrypt()
    assert decrypted == "decrypted"

def test_secret_name():
    secret = store_secret("my_secret_name", "data")
    assert secret.name == "my_secret_name"

def test_secret_value():
    secret = store_secret("name", "the_value")
    assert secret.encrypted_value == "the_value"
