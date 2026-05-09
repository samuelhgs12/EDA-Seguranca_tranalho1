"""Operações de assinatura digital RSA com SHA-512."""

from __future__ import annotations

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


# Padding de assinatura RSA recomendado para compatibilidade com enunciado
RSA_SIGNATURE_PADDING = padding.PKCS1v15()


def sign_sha512_rsa(plaintext: bytes, private_key) -> bytes:
    """Assina o texto claro com SHA-512 e RSA.

    Observação importante: a assinatura é feita sobre o texto em claro,
    conforme exigência do trabalho.
    """
    return private_key.sign(plaintext, RSA_SIGNATURE_PADDING, hashes.SHA512())


def verify_sha512_rsa(plaintext: bytes, signature: bytes, public_key) -> bool:
    """Verifica assinatura RSA+SHA-512 e retorna True/False sem abortar fluxo."""
    try:
        public_key.verify(signature, plaintext, RSA_SIGNATURE_PADDING, hashes.SHA512())
        return True
    except InvalidSignature:
        return False
