"""AES encryption/decryption helpers."""

from __future__ import annotations

import secrets


def generate_aes128_key_iv() -> tuple[bytes, bytes]:
    return secrets.token_bytes(16), secrets.token_bytes(16)


def aes_encrypt_cbc_pkcs7(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    raise NotImplementedError("Implement AES-128-CBC encryption with PKCS7 padding")


def aes_decrypt_cbc_pkcs7(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    raise NotImplementedError("Implement AES-128-CBC decryption with PKCS7 padding")
