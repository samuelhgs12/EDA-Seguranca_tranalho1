from __future__ import annotations

import secrets

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_aes128_key_iv() -> tuple[bytes, bytes]:
    return secrets.token_bytes(16), secrets.token_bytes(16)


def aes_encrypt_cbc_pkcs7(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    if len(key) != 16 or len(iv) != 16:
        raise ValueError("AES-128 requires 16-byte key and 16-byte IV")

    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(padded) + encryptor.finalize()


def aes_decrypt_cbc_pkcs7(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    if len(key) != 16 or len(iv) != 16:
        raise ValueError("AES-128 requires 16-byte key and 16-byte IV")

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()
