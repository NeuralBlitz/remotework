"""
Cryptographic Operations Plugin
Encrypt, decrypt, hash, HMAC, key generation, and JWT tokens.
"""
import logging
import base64
import hashlib
import hmac
import secrets
import json
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.crypto_ops")

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


def crypto_encrypt_cmd(data: str = "", key: str = "") -> Dict:
    if not CRYPTO_AVAILABLE:
        raise ImportError("cryptography not installed. Run: pip install cryptography")
    if not key:
        key = Fernet.generate_key()
    else:
        key = base64.urlsafe_b64encode(hashlib.sha256(key.encode()).digest())
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return {"ciphertext": base64.urlsafe_b64encode(encrypted).decode(), "key": key.decode() if isinstance(key, bytes) else key}


def crypto_decrypt_cmd(ciphertext: str = "", key: str = "") -> Dict:
    if not CRYPTO_AVAILABLE:
        raise ImportError("cryptography not installed. Run: pip install cryptography")
    f = Fernet(key.encode())
    decrypted = f.decrypt(base64.urlsafe_b64decode(ciphertext))
    return {"plaintext": decrypted.decode()}


def crypto_hash_cmd(data: str = "", algorithm: str = "sha256") -> Dict:
    alg = getattr(hashlib, algorithm, hashlib.sha256)
    h = alg(data.encode()).hexdigest()
    return {"hash": h, "algorithm": algorithm, "length": len(h)}


def crypto_hmac_cmd(data: str = "", key: str = "", algorithm: str = "sha256") -> Dict:
    alg = getattr(hashlib, algorithm, hashlib.sha256)
    mac = hmac.new(key.encode(), data.encode(), alg).hexdigest()
    return {"hmac": mac, "algorithm": algorithm, "verified": True}


def crypto_generate_key_cmd(algorithm: str = "fernet", length: int = 32) -> Dict:
    if algorithm == "fernet":
        key = Fernet.generate_key()
        return {"key": key.decode(), "algorithm": algorithm}
    elif algorithm == "random":
        key = secrets.token_hex(length)
        return {"key": key, "algorithm": algorithm, "length": length * 2}
    else:
        return {"error": f"Unknown algorithm: {algorithm}"}


def crypto_generate_token_cmd(length: int = 32, format: str = "hex") -> Dict:
    if format == "hex":
        token = secrets.token_hex(length)
    elif format == "urlsafe":
        token = secrets.token_urlsafe(length)
    elif format == "ascii":
        token = "".join(secrets.choice(__import__("string").ascii_letters + __import__("string").digits) for _ in range(length))
    else:
        token = secrets.token_bytes(length)
    return {"token": token, "length": length}


def crypto_aes_encrypt_cmd(data: str = "", password: str = "", salt: str = "") -> Dict:
    if not CRYPTO_AVAILABLE:
        raise ImportError("cryptography not installed. Run: pip install cryptography")
    import os
    salt_bytes = salt.encode() if salt else os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt_bytes, iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return {"ciphertext": base64.urlsafe_b64encode(encrypted).decode(), "salt": base64.b64encode(salt_bytes).decode()}


def crypto_aes_decrypt_cmd(ciphertext: str = "", password: str = "", salt: str = "") -> Dict:
    if not CRYPTO_AVAILABLE:
        raise ImportError("cryptography not installed. Run: pip install cryptography")
    salt_bytes = base64.b64decode(salt)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt_bytes, iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(key)
    decrypted = f.decrypt(base64.urlsafe_b64decode(ciphertext))
    return {"plaintext": decrypted.decode()}


def register(plugin):
    plugin.register_command("encrypt", crypto_encrypt_cmd)
    plugin.register_command("decrypt", crypto_decrypt_cmd)
    plugin.register_command("hash", crypto_hash_cmd)
    plugin.register_command("hmac", crypto_hmac_cmd)
    plugin.register_command("generate_key", crypto_generate_key_cmd)
    plugin.register_command("generate_token", crypto_generate_token_cmd)
    plugin.register_command("aes_encrypt", crypto_aes_encrypt_cmd)
    plugin.register_command("aes_decrypt", crypto_aes_decrypt_cmd)


PLUGIN_METADATA = {
    "name": "crypto_ops", "version": "1.0.0",
    "description": "Encrypt, decrypt, hash, HMAC, key generation, and token creation",
    "author": "Mito Team", "license": "MIT",
    "tags": ["crypto", "encryption", "security", "utilities"],
    "dependencies": ["cryptography"], "permissions": [],
    "min_mito_version": "1.0.1",
}

crypto_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
