from __future__ import annotations

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def assinar_sha512_rsa(texto_claro: bytes, chave_privada) -> bytes:
    return chave_privada.sign(texto_claro, padding.PKCS1v15(), hashes.SHA512())


def verificar_sha512_rsa(texto_claro: bytes, assinatura: bytes, chave_publica) -> bool:
    try:
        chave_publica.verify(assinatura, texto_claro, padding.PKCS1v15(), hashes.SHA512())
    except InvalidSignature:
        return False
    return True
