"""RSA key generation and RSA encrypt/decrypt helpers."""

from __future__ import annotations


def generate_rsa_keypair_pem(bits: int) -> tuple[bytes, bytes]:
    raise NotImplementedError("Implement RSA key pair generation in PEM format")


def load_public_key(pem_data: bytes):
    raise NotImplementedError("Implement PEM public key loading")


def load_private_key(pem_data: bytes):
    raise NotImplementedError("Implement PEM private key loading")


def rsa_encrypt_pkcs1v15(data: bytes, public_key) -> bytes:
    raise NotImplementedError("Implement RSA encryption with PKCS1v15")


def rsa_decrypt_pkcs1v15(ciphertext: bytes, private_key) -> bytes:
    raise NotImplementedError("Implement RSA decryption with PKCS1v15")
