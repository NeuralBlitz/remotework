"""
Mito Crypto Utilities
Hashing, encryption, tokens, JWT, HMAC, signing, key derivation, AES
"""

import hashlib
import hmac as hmac_mod
import base64
import secrets
import json
import time
import os
import struct
from typing import Dict, Optional, Any, List, Tuple
from pathlib import Path


# ========== Hashing ==========

def sha256(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def sha512(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha512(data).hexdigest()


def sha1(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha1(data).hexdigest()


def sha3_256(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha3_256(data).hexdigest()


def sha3_512(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha3_512(data).hexdigest()


def blake2b(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.blake2b(data).hexdigest()


def blake2s(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.blake2s(data).hexdigest()


def md5(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.md5(data).hexdigest()


def hash_with_salt(data: str, salt: str = None, algo: str = "sha256") -> Tuple[str, str]:
    salt = salt or secrets.token_hex(16)
    h = hashlib.new(algo)
    h.update((data + salt).encode())
    return h.hexdigest(), salt


def verify_with_salt(data: str, hashed: str, salt: str, algo: str = "sha256") -> bool:
    h = hashlib.new(algo)
    h.update((data + salt).encode())
    return h.hexdigest() == hashed


# ========== Password Hashing ==========

def bcrypt_hash(password: str) -> str:
    import bcrypt
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def bcrypt_verify(password: str, hashed: str) -> bool:
    import bcrypt
    return bcrypt.checkpw(password.encode(), hashed.encode())


def argon2_hash(password: str) -> str:
    try:
        from argon2 import PasswordHasher
        ph = PasswordHasher()
        return ph.hash(password)
    except ImportError:
        raise ImportError("argon2-cffi not installed")


def argon2_verify(password: str, hashed: str) -> bool:
    try:
        from argon2 import PasswordHasher
        ph = PasswordHasher()
        return ph.verify(hashed, password)
    except Exception:
        return False


def scrypt_hash(password: str, salt: bytes = None, n: int = 16384, r: int = 8, p: int = 1) -> str:
    salt = salt or os.urandom(16)
    key = hashlib.scrypt(password.encode(), salt=salt, n=n, r=r, p=p)
    return base64.b64encode(salt + key).decode()


def scrypt_verify(password: str, hashed: str) -> bool:
    decoded = base64.b64decode(hashed)
    salt = decoded[:16]
    stored_key = decoded[16:]
    key = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1)
    return key == stored_key


# ========== HMAC ==========

def hmac_sign(data: str | bytes, secret: str | bytes, algo: str = "sha256") -> str:
    if isinstance(data, str):
        data = data.encode()
    if isinstance(secret, str):
        secret = secret.encode()
    return hmac_mod.new(secret, data, getattr(hashlib, algo)).hexdigest()


def hmac_verify(data: str | bytes, secret: str | bytes, signature: str, algo: str = "sha256") -> bool:
    expected = hmac_sign(data, secret, algo)
    return hmac_mod.compare_digest(expected, signature)


def hmac_base64(data: str | bytes, secret: str | bytes, algo: str = "sha256") -> str:
    if isinstance(data, str):
        data = data.encode()
    if isinstance(secret, str):
        secret = secret.encode()
    return base64.b64encode(hmac_mod.new(secret, data, getattr(hashlib, algo)).digest()).decode()


# ========== Token Generation ==========

def generate_token(nbytes: int = 32) -> str:
    return secrets.token_urlsafe(nbytes)


def generate_hex_token(nbytes: int = 32) -> str:
    return secrets.token_hex(nbytes)


def generate_numeric_code(length: int = 6) -> str:
    return "".join(str(secrets.randbelow(10)) for _ in range(length))


def generate_api_key(prefix: str = "mk", nbytes: int = 32) -> str:
    return f"{prefix}_{secrets.token_urlsafe(nbytes)}"


def generate_otp(length: int = 6, alphanumeric: bool = False) -> str:
    if alphanumeric:
        chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        return "".join(secrets.choice(chars) for _ in range(length))
    return generate_numeric_code(length)


def generate_uuid() -> str:
    import uuid
    return str(uuid.uuid4())


def generate_nanoid(length: int = 21) -> str:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
    return "".join(secrets.choice(alphabet) for _ in range(length))


# ========== Base64 ==========

def encode_base64(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return base64.b64encode(data).decode()


def decode_base64(data: str) -> bytes:
    return base64.b64decode(data)


def encode_url64(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return base64.urlsafe_b64encode(data).decode()


def decode_url64(data: str) -> bytes:
    return base64.urlsafe_b64decode(data)


# ========== JWT ==========

def jwt_encode(payload: Dict, secret: str, algorithm: str = "HS256", expires_in: int = 0,
               issuer: str = "", audience: str = "") -> str:
    header = {"alg": algorithm, "typ": "JWT"}
    now = int(time.time())

    if expires_in:
        payload = {**payload, "exp": now + expires_in}
    if issuer:
        payload = {**payload, "iss": issuer}
    if audience:
        payload = {**payload, "aud": audience}
    if "iat" not in payload:
        payload = {**payload, "iat": now}

    header_b64 = encode_url64(json.dumps(header, separators=(",", ":")))
    payload_b64 = encode_url64(json.dumps(payload, separators=(",", ":")))
    signing_input = f"{header_b64}.{payload_b64}"
    signature = hmac_sign(signing_input, secret, "sha256")
    sig_b64 = encode_url64(signature)
    return f"{header_b64}.{payload_b64}.{sig_b64}"


def jwt_decode(token: str, secret: str = None, verify_exp: bool = True,
               issuer: str = None, audience: str = None) -> Dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")

    header_b64, payload_b64, sig_b64 = parts

    if secret:
        signing_input = f"{header_b64}.{payload_b64}"
        expected_sig = hmac_sign(signing_input, secret, "sha256")
        actual_sig = decode_url64(sig_b64).decode()
        if not hmac_mod.compare_digest(expected_sig, actual_sig):
            raise ValueError("Invalid JWT signature")

    payload = json.loads(decode_base64(payload_b64))

    if verify_exp and "exp" in payload and payload["exp"] < time.time():
        raise ValueError("JWT expired")

    if issuer and payload.get("iss") != issuer:
        raise ValueError("Invalid JWT issuer")

    if audience and payload.get("aud") != audience:
        raise ValueError("Invalid JWT audience")

    return payload


def jwt_get_claims(token: str) -> Dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")
    return json.loads(decode_base64(parts[1]))


# ========== Encryption (AES via Fernet) ==========

def generate_aes_key() -> bytes:
    return os.urandom(32)


def generate_fernet_key() -> str:
    from cryptography.fernet import Fernet
    return Fernet.generate_key().decode()


def fernet_encrypt(data: str | bytes, key: str) -> str:
    from cryptography.fernet import Fernet
    if isinstance(data, str):
        data = data.encode()
    f = Fernet(key.encode() if isinstance(key, str) else key)
    return f.encrypt(data).decode()


def fernet_decrypt(data: str, key: str) -> str:
    from cryptography.fernet import Fernet
    f = Fernet(key.encode() if isinstance(key, str) else key)
    return f.decrypt(data.encode()).decode()


def aes_encrypt(data: str | bytes, key: bytes = None) -> Tuple[bytes, bytes, bytes]:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend

    if isinstance(data, str):
        data = data.encode()
    key = key or os.urandom(32)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    pad_len = 16 - (len(data) % 16)
    padded = data + bytes([pad_len] * pad_len)
    encrypted = encryptor.update(padded) + encryptor.finalize()

    return encrypted, key, iv


def aes_decrypt(encrypted: bytes, key: bytes, iv: bytes) -> bytes:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded = decryptor.update(encrypted) + decryptor.finalize()

    pad_len = padded[-1]
    return padded[:-pad_len]


# ========== Key Derivation ==========

def derive_key_pbkdf2(password: str, salt: bytes = None, iterations: int = 100000,
                      key_length: int = 32) -> Tuple[bytes, bytes]:
    salt = salt or os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations, dklen=key_length)
    return key, salt


def derive_key_hkdf(password: str, salt: bytes = None, info: bytes = b"mito",
                    length: int = 32) -> bytes:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF

    salt = salt or os.urandom(16)
    hkdf = HKDF(algorithm=hashes.SHA256(), length=length, salt=salt, info=info)
    return hkdf.derive(password.encode())


# ========== Utility ==========

def constant_time_compare(a: str, b: str) -> bool:
    return hmac_mod.compare_digest(a, b)


def hash_file(filepath: str, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def hash_multiple(filepath: str, algos: List[str] = None) -> Dict[str, str]:
    algos = algos or ["md5", "sha1", "sha256", "sha512"]
    hashers = {algo: hashlib.new(algo) for algo in algos}
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            for h in hashers.values():
                h.update(chunk)
    return {algo: h.hexdigest() for algo, h in hashers.items()}


def crc32(data: str | bytes) -> int:
    if isinstance(data, str):
        data = data.encode()
    import zlib
    return zlib.crc32(data) & 0xFFFFFFFF


def adler32(data: str | bytes) -> int:
    if isinstance(data, str):
        data = data.encode()
    import zlib
    return zlib.adler32(data) & 0xFFFFFFFF


def entropy(data: str) -> float:
    import math
    freq = {}
    for c in data:
        freq[c] = freq.get(c, 0) + 1
    length = len(data)
    return -sum((count/length) * math.log2(count/length) for count in freq.values())


def password_strength(password: str) -> Dict:
    score = 0
    checks = {
        "length_8": len(password) >= 8,
        "length_12": len(password) >= 12,
        "length_16": len(password) >= 16,
        "uppercase": any(c.isupper() for c in password),
        "lowercase": any(c.islower() for c in password),
        "digit": any(c.isdigit() for c in password),
        "special": any(not c.isalnum() for c in password),
        "no_common": password.lower() not in ("password", "123456", "qwerty", "admin"),
    }
    score = sum(checks.values())
    strength = "weak" if score < 4 else "medium" if score < 6 else "strong" if score < 7 else "very_strong"
    return {"score": score, "max_score": 8, "strength": strength, "checks": checks}
