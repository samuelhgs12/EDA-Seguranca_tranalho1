from __future__ import annotations

import argparse


class AnalisadorArgumentos(argparse.ArgumentParser):
    def format_usage(self) -> str:
        return super().format_usage().replace("usage:", "uso:")

    def format_help(self) -> str:
        return (
            super()
            .format_help()
            .replace("usage:", "uso:")
            .replace("positional arguments:", "argumentos posicionais:")
            .replace("options:", "opções:")
            .replace("show this help message and exit", "mostrar esta mensagem de ajuda e sair")
        )

    def error(self, mensagem: str) -> None:
        mensagem = (
            mensagem.replace("the following arguments are required:", "os seguintes argumentos são obrigatórios:")
            .replace("invalid choice", "opção inválida")
            .replace("choose from", "escolha entre")
            .replace("expected one argument", "esperado um argumento")
        )
        self.print_usage()
        self.exit(2, f"{self.prog}: erro: {mensagem}\n")


def _criar_analisador(*args, **kwargs) -> AnalisadorArgumentos:
    return AnalisadorArgumentos(*args, add_help=False, **kwargs)


def construir_analisador() -> argparse.ArgumentParser:
    analisador = _criar_analisador(prog="envelope-digital")
    analisador.add_argument("-h", "--ajuda", action="help", help="mostrar esta mensagem de ajuda e sair")
    subanalisadores = analisador.add_subparsers(
        dest="comando", required=True, metavar="comando", parser_class=AnalisadorArgumentos
    )

    gerador_chaves = subanalisadores.add_parser(
        "gerar-chaves",
        help="Gerar par de chaves RSA PEM",
        add_help=False
    )
    gerador_chaves.add_argument("-h", "--ajuda", action="help", help="mostrar esta mensagem de ajuda e sair")
    gerador_chaves.add_argument("--tamanho", type=int, choices=[1024, 2048], required=True, metavar="TAMANHO")
    gerador_chaves.add_argument("--privada-saida", required=True, metavar="CAMINHO")
    gerador_chaves.add_argument("--publica-saida", required=True, metavar="CAMINHO")

    criador_envelope = subanalisadores.add_parser(
        "criar-envelope",
        help="Criar envelope (.cif/.env/.sig)",
        add_help=False
    )
    criador_envelope.add_argument("-h", "--ajuda", action="help", help="mostrar esta mensagem de ajuda e sair")
    criador_envelope.add_argument("--entrada", required=True, metavar="ARQUIVO")
    criador_envelope.add_argument("--dest-publica", required=True, metavar="CHAVE")
    criador_envelope.add_argument("--remet-privada", required=True, metavar="CHAVE")
    criador_envelope.add_argument("--diretorio-saida", default="envelope", metavar="DIRETORIO")
    criador_envelope.add_argument("--nome-base", default="envelope", metavar="NOME")

    abridor_envelope = subanalisadores.add_parser(
        "abrir-envelope",
        help="Abrir envelope e verificar assinatura",
        add_help=False
    )
    abridor_envelope.add_argument("-h", "--ajuda", action="help", help="mostrar esta mensagem de ajuda e sair")
    abridor_envelope.add_argument("--cif", required=True, metavar="ARQUIVO")
    abridor_envelope.add_argument("--env", required=True, metavar="ARQUIVO")
    abridor_envelope.add_argument("--sig", required=True, metavar="ARQUIVO")
    abridor_envelope.add_argument("--dest-privada", required=True, metavar="CHAVE")
    abridor_envelope.add_argument("--remet-publica", required=True, metavar="CHAVE")
    abridor_envelope.add_argument("--saida-claro", required=True, metavar="ARQUIVO")

    return analisador
