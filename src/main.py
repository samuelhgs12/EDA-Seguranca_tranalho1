from __future__ import annotations

from pathlib import Path

from cli import build_parser
from crypto.envelope_ops import EnvelopeArtifacts, build_envelope_paths, create_envelope, open_envelope
from crypto.rsa_ops import generate_rsa_keypair_pem, load_private_key, load_public_key
from utils.file_io import write_text_file


def _read_bytes(path: str | Path) -> bytes:
    return Path(path).read_bytes()


def _write_bytes(path: str | Path, data: bytes) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def _resolve_key_output(path: str | Path, keys_dir: str | Path = "keys") -> Path:
    target = Path(path)
    if target.is_absolute():
        return target
    if target.parent == Path("."):
        return Path(keys_dir) / target.name
    return target


def main() -> int:
    args = build_parser().parse_args()

    try:
        if args.command == "gen-keys":
            private_pem, public_pem = generate_rsa_keypair_pem(args.bits)
            private_path = _resolve_key_output(args.private_out)
            public_path = _resolve_key_output(args.public_out)
            _write_bytes(private_path, private_pem)
            _write_bytes(public_path, public_pem)
            print("Chaves RSA geradas com sucesso.")
            print(f"Privada: {private_path}")
            print(f"Publica: {public_path}")
            return 0

        if args.command == "seal":
            recipient_public_key = load_public_key(_read_bytes(args.dest_pub))
            sender_private_key = load_private_key(_read_bytes(args.sender_priv))
            artifacts = build_envelope_paths(args.base_name, args.out_dir)
            create_envelope(args.infile, recipient_public_key, sender_private_key, artifacts)
            print("Envelope criado com sucesso.")
            print(f"Mensagem cifrada: {artifacts.encrypted_message}")
            print(f"Chave+IV cifrados: {artifacts.encrypted_session}")
            print(f"Assinatura: {artifacts.signature}")
            return 0

        if args.command == "open":
            artifacts = EnvelopeArtifacts(
                encrypted_message=Path(args.cif),
                encrypted_session=Path(args.env),
                signature=Path(args.sig),
            )
            recipient_private_key = load_private_key(_read_bytes(args.dest_priv))
            sender_public_key = load_public_key(_read_bytes(args.sender_pub))
            plaintext, valid, key_hex, iv_hex = open_envelope(
                artifacts, recipient_private_key, sender_public_key
            )
            write_text_file(args.out_plain, plaintext)
            print("Envelope aberto com sucesso.")
            print(f"Chave AES (hex): {key_hex}")
            print(f"IV AES (hex): {iv_hex}")
            print(f"Assinatura valida: {'sim' if valid else 'nao'}")
            print(f"Texto em claro: {args.out_plain}")
            return 0

        print(f"Comando desconhecido: {args.command}")
        return 1
    except Exception as exc:  
        print(f"Erro: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
