from __future__ import annotations

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def gerar_par_chaves_rsa_pem(tamanho_bits: int) -> tuple[bytes, bytes]:
    if tamanho_bits not in (1024, 2048):
        raise ValueError("O tamanho da chave RSA deve ser 1024 ou 2048 bits")

    chave_privada = rsa.generate_private_key(public_exponent=65537, key_size=tamanho_bits)
    chave_publica = chave_privada.public_key()

    pem_privado = chave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pem_publico = chave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem_privado, pem_publico


def carregar_chave_publica(dados_pem: bytes):
    return serialization.load_pem_public_key(dados_pem)


def carregar_chave_privada(dados_pem: bytes):
    return serialization.load_pem_private_key(dados_pem, password=None)


def cifrar_rsa_pkcs1v15(dados: bytes, chave_publica) -> bytes:
    return chave_publica.encrypt(dados, padding.PKCS1v15())


def decifrar_rsa_pkcs1v15(texto_cifrado: bytes, chave_privada) -> bytes:
    return chave_privada.decrypt(texto_cifrado, padding.PKCS1v15())
