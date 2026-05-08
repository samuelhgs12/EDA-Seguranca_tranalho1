"""Envelope file naming conventions and orchestration helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from crypto.aes_ops import aes_decrypt_cbc_pkcs7, aes_encrypt_cbc_pkcs7, generate_aes128_key_iv
from crypto.rsa_ops import rsa_decrypt_pkcs1v15, rsa_encrypt_pkcs1v15
from crypto.signature_ops import sign_sha512_rsa, verify_sha512_rsa
from utils.encoding import from_base64, pack_key_iv_hex, to_base64, unpack_key_iv_hex
from utils.file_io import read_text_file, write_text_file
from utils.validators import ensure_supported_envelope_extension


@dataclass(frozen=True)
class EnvelopeArtifacts:
    encrypted_message: Path
    encrypted_session: Path
    signature: Path


def build_envelope_paths(base_name: str, output_dir: str | Path = ".") -> EnvelopeArtifacts:
    root = Path(output_dir)
    return EnvelopeArtifacts(
        encrypted_message=root / f"{base_name}.cif",
        encrypted_session=root / f"{base_name}.env",
        signature=root / f"{base_name}.sig",
    )


def validate_artifact_paths(artifacts: EnvelopeArtifacts) -> None:
    ensure_supported_envelope_extension(artifacts.encrypted_message, ".cif")
    ensure_supported_envelope_extension(artifacts.encrypted_session, ".env")
    ensure_supported_envelope_extension(artifacts.signature, ".sig")


def create_envelope(
    plaintext_path: str | Path,
    recipient_public_key,
    sender_private_key,
    artifacts: EnvelopeArtifacts,
) -> None:
    validate_artifact_paths(artifacts)
    plaintext = read_text_file(plaintext_path).encode("utf-8")
    key, iv = generate_aes128_key_iv()

    ciphertext = aes_encrypt_cbc_pkcs7(plaintext, key, iv)
    packed_hex = pack_key_iv_hex(key, iv)
    encrypted_session = rsa_encrypt_pkcs1v15(packed_hex.encode("ascii"), recipient_public_key)
    signature = sign_sha512_rsa(plaintext, sender_private_key)

    write_text_file(artifacts.encrypted_message, to_base64(ciphertext))
    write_text_file(artifacts.encrypted_session, to_base64(encrypted_session))
    write_text_file(artifacts.signature, to_base64(signature))


def open_envelope(
    artifacts: EnvelopeArtifacts,
    recipient_private_key,
    sender_public_key,
) -> tuple[str, bool, str, str]:
    validate_artifact_paths(artifacts)

    ciphertext = from_base64(read_text_file(artifacts.encrypted_message).strip())
    encrypted_session = from_base64(read_text_file(artifacts.encrypted_session).strip())
    signature = from_base64(read_text_file(artifacts.signature).strip())

    packed_hex = rsa_decrypt_pkcs1v15(encrypted_session, recipient_private_key).decode("ascii")
    key, iv = unpack_key_iv_hex(packed_hex)

    plaintext = aes_decrypt_cbc_pkcs7(ciphertext, key, iv)
    valid = verify_sha512_rsa(plaintext, signature, sender_public_key)

    return plaintext.decode("utf-8"), valid, key.hex(), iv.hex()
