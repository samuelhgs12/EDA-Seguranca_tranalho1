"""Operações RSA para geração de chaves e cifra/decifra da sessão."""

from __future__ import annotations

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


# Padding definido no enunciado para cifra RSA (equivalente a ECB/PKCS1Padding em Java)
RSA_CIPHER_PADDING = padding.PKCS1v15()


def generate_rsa_keypair_pem(bits: int) -> tuple[bytes, bytes]:
    """Gera par de chaves RSA em PEM compatível com OpenSSL.

    Args:
        bits: Tamanho da chave (1024 ou 2048).

    Returns:
        Tupla (private_pem, public_pem) em bytes.
    """

    if bits not in (1024, 2048):
        raise ValueError("bits deve ser 1024 ou 2048")

    # Geração da chave privada RSA com expoente público padrão 65537
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=bits)
    public_key = private_key.public_key()

    # Serializa chave privada no formato PEM PKCS8 sem senha (como solicitado)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Serializa chave pública em PEM SubjectPublicKeyInfo (padrão OpenSSL)
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def load_public_key(pem_data: bytes):
    """Carrega uma chave pública RSA a partir de PEM."""
    return serialization.load_pem_public_key(pem_data)


def load_private_key(pem_data: bytes):
    """Carrega uma chave privada RSA a partir de PEM sem senha."""
    return serialization.load_pem_private_key(pem_data, password=None)


def rsa_encrypt_pkcs1v15(data: bytes, public_key) -> bytes:
    """Cifra bytes com RSA PKCS#1 v1.5 usando a chave pública do destinatário."""
    return public_key.encrypt(data, RSA_CIPHER_PADDING)


def rsa_decrypt_pkcs1v15(ciphertext: bytes, private_key) -> bytes:
    """Decifra bytes com RSA PKCS#1 v1.5 usando a chave privada do destinatário."""
    return private_key.decrypt(ciphertext, RSA_CIPHER_PADDING)
