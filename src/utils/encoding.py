from __future__ import annotations

import base64


def to_base64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def from_base64(text: str) -> bytes:
    return base64.b64decode(text.encode("ascii"), validate=True)


def to_hex(data: bytes) -> str:
    return data.hex()


def from_hex(text: str) -> bytes:
    return bytes.fromhex(text)


def pack_key_iv_hex(key: bytes, iv: bytes) -> str:
    if len(key) != 16 or len(iv) != 16:
        raise ValueError("AES-128 requires 16-byte key and 16-byte IV")
    return f"{to_hex(key)}{to_hex(iv)}"


def unpack_key_iv_hex(packed_hex: str) -> tuple[bytes, bytes]:
    if len(packed_hex) != 64:
        raise ValueError("Packed key+iv hex must contain 64 hex chars")
    return from_hex(packed_hex[:32]), from_hex(packed_hex[32:])
