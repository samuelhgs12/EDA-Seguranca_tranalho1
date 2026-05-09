from __future__ import annotations

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def generate_rsa_keypair_pem(bits: int) -> tuple[bytes, bytes]:
    if bits not in (1024, 2048):
        raise ValueError("RSA bits must be 1024 or 2048")

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=bits)
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def load_public_key(pem_data: bytes):
    return serialization.load_pem_public_key(pem_data)


def load_private_key(pem_data: bytes):
    return serialization.load_pem_private_key(pem_data, password=None)


def rsa_encrypt_pkcs1v15(data: bytes, public_key) -> bytes:
    return public_key.encrypt(data, padding.PKCS1v15())


def rsa_decrypt_pkcs1v15(ciphertext: bytes, private_key) -> bytes:
    return private_key.decrypt(ciphertext, padding.PKCS1v15())
