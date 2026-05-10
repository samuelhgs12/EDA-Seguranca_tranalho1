from __future__ import annotations
import secrets
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def gerar_chave_iv_aes128() -> tuple[bytes, bytes]:
    return secrets.token_bytes(16), secrets.token_bytes(16)


def cifrar_aes_cbc_pkcs7(texto_claro: bytes, chave: bytes, iv: bytes) -> bytes:
    if len(chave) != 16 or len(iv) != 16:
        raise ValueError("AES-128 exige chave e IV com 16 bytes")

    preenchedor = padding.PKCS7(128).padder()
    texto_preenchido = preenchedor.update(texto_claro) + preenchedor.finalize()

    cifra = Cipher(algorithms.AES(chave), modes.CBC(iv))
    cifrador = cifra.encryptor()
    return cifrador.update(texto_preenchido) + cifrador.finalize()


def decifrar_aes_cbc_pkcs7(texto_cifrado: bytes, chave: bytes, iv: bytes) -> bytes:
    if len(chave) != 16 or len(iv) != 16:
        raise ValueError("AES-128 exige chave e IV com 16 bytes")

    cifra = Cipher(algorithms.AES(chave), modes.CBC(iv))
    decifrador = cifra.decryptor()
    texto_preenchido = decifrador.update(texto_cifrado) + decifrador.finalize()

    removedor_preenchimento = padding.PKCS7(128).unpadder()
    return removedor_preenchimento.update(texto_preenchido) + removedor_preenchimento.finalize()
