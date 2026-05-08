"""Command-line interface wiring for assignment conventions."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="envelope-digital")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_keys = subparsers.add_parser("gen-keys", help="Gerar par de chaves RSA PEM")
    p_keys.add_argument("--bits", type=int, choices=[1024, 2048], required=True)
    p_keys.add_argument("--private-out", required=True)
    p_keys.add_argument("--public-out", required=True)

    p_seal = subparsers.add_parser("seal", help="Criar envelope (.cif/.env/.sig)")
    p_seal.add_argument("--in", dest="infile", required=True)
    p_seal.add_argument("--dest-pub", required=True)
    p_seal.add_argument("--sender-priv", required=True)
    p_seal.add_argument("--out-dir", default=".")
    p_seal.add_argument("--base-name", default="envelope")

    p_open = subparsers.add_parser("open", help="Abrir envelope e verificar assinatura")
    p_open.add_argument("--cif", required=True)
    p_open.add_argument("--env", required=True)
    p_open.add_argument("--sig", required=True)
    p_open.add_argument("--dest-priv", required=True)
    p_open.add_argument("--sender-pub", required=True)
    p_open.add_argument("--out-plain", required=True)

    return parser
