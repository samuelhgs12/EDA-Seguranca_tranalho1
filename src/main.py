"""CLI entrypoint module."""

from __future__ import annotations

from cli import build_parser


def main() -> int:
    args = build_parser().parse_args()
    print(f"Comando recebido: {args.command}. Implementação criptográfica pendente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
