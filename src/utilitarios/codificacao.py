from __future__ import annotations

import base64


def para_base64(dados: bytes) -> str:
    return base64.b64encode(dados).decode("ascii")


def de_base64(texto: str) -> bytes:
    return base64.b64decode(texto.encode("ascii"), validate=True)


def para_hex(dados: bytes) -> str:
    return dados.hex()


def de_hex(texto: str) -> bytes:
    return bytes.fromhex(texto)


def empacotar_chave_iv_hex(chave: bytes, iv: bytes) -> str:
    if len(chave) != 16 or len(iv) != 16:
        raise ValueError("AES-128 exige chave e IV com 16 bytes")
    return f"{para_hex(chave)}{para_hex(iv)}"


def desempacotar_chave_iv_hex(hex_empacotado: str) -> tuple[bytes, bytes]:
    if len(hex_empacotado) != 64:
        raise ValueError("Chave+IV empacotados em HEX devem conter 64 caracteres")
    return de_hex(hex_empacotado[:32]), de_hex(hex_empacotado[32:])
