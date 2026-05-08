"""Digital signature and verification helpers."""

from __future__ import annotations


def sign_sha512_rsa(plaintext: bytes, private_key) -> bytes:
    raise NotImplementedError("Implement RSA signature with SHA-512")


def verify_sha512_rsa(plaintext: bytes, signature: bytes, public_key) -> bool:
    raise NotImplementedError("Implement RSA signature verification with SHA-512")
