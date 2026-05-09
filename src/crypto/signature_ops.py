from __future__ import annotations

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def sign_sha512_rsa(plaintext: bytes, private_key) -> bytes:
    return private_key.sign(plaintext, padding.PKCS1v15(), hashes.SHA512())


def verify_sha512_rsa(plaintext: bytes, signature: bytes, public_key) -> bool:
    try:
        public_key.verify(signature, plaintext, padding.PKCS1v15(), hashes.SHA512())
    except InvalidSignature:
        return False
    return True
