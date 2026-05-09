from __future__ import annotations

from pathlib import Path

from criptografia.operacoes_envelope import (
    ArtefatosEnvelope,
    abrir_envelope,
    criar_caminhos_envelope,
    criar_envelope,
)
from criptografia.operacoes_rsa import (
    carregar_chave_privada,
    carregar_chave_publica,
    gerar_par_chaves_rsa_pem,
)
from interface_linha_comando import construir_analisador
from utilitarios.arquivos import gravar_arquivo_texto


def _ler_bytes(caminho: str | Path) -> bytes:
    return Path(caminho).read_bytes()


def _gravar_bytes(caminho: str | Path, dados: bytes) -> None:
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(dados)


def _resolver_saida_chave(caminho: str | Path, diretorio_chaves: str | Path = "chaves") -> Path:
    destino = Path(caminho)
    if destino.is_absolute():
        return destino
    if destino.parent == Path("."):
        return Path(diretorio_chaves) / destino.name
    return destino


def principal() -> int:
    argumentos = construir_analisador().parse_args()

    try:
        if argumentos.comando == "gerar-chaves":
            pem_privado, pem_publico = gerar_par_chaves_rsa_pem(argumentos.tamanho)
            caminho_privado = _resolver_saida_chave(argumentos.privada_saida)
            caminho_publico = _resolver_saida_chave(argumentos.publica_saida)
            _gravar_bytes(caminho_privado, pem_privado)
            _gravar_bytes(caminho_publico, pem_publico)
            print("Chaves RSA geradas com sucesso.")
            print(f"Privada: {caminho_privado}")
            print(f"Pública: {caminho_publico}")
            return 0

        if argumentos.comando == "criar-envelope":
            chave_publica_destinatario = carregar_chave_publica(_ler_bytes(argumentos.dest_publica))
            chave_privada_remetente = carregar_chave_privada(_ler_bytes(argumentos.remet_privada))
            artefatos = criar_caminhos_envelope(argumentos.nome_base, argumentos.diretorio_saida)
            criar_envelope(
                argumentos.entrada,
                chave_publica_destinatario,
                chave_privada_remetente,
                artefatos,
            )
            print("Envelope criado com sucesso.")
            print(f"Mensagem cifrada: {artefatos.mensagem_cifrada}")
            print(f"Chave+IV cifrados: {artefatos.sessao_cifrada}")
            print(f"Assinatura: {artefatos.assinatura}")
            return 0

        if argumentos.comando == "abrir-envelope":
            artefatos = ArtefatosEnvelope(
                mensagem_cifrada=Path(argumentos.cif),
                sessao_cifrada=Path(argumentos.env),
                assinatura=Path(argumentos.sig),
            )
            chave_privada_destinatario = carregar_chave_privada(_ler_bytes(argumentos.dest_privada))
            chave_publica_remetente = carregar_chave_publica(_ler_bytes(argumentos.remet_publica))
            texto_claro, assinatura_valida, chave_hex, iv_hex = abrir_envelope(
                artefatos,
                chave_privada_destinatario,
                chave_publica_remetente,
            )
            gravar_arquivo_texto(argumentos.saida_claro, texto_claro)
            print("Envelope aberto com sucesso.")
            print(f"Chave AES (hex): {chave_hex}")
            print(f"IV AES (hex): {iv_hex}")
            print(f"Assinatura válida: {'sim' if assinatura_valida else 'não'}")
            print(f"Texto em claro: {argumentos.saida_claro}")
            return 0

        print(f"Comando desconhecido: {argumentos.comando}")
        return 1
    except Exception as erro:
        print(f"Erro: {erro}")
        return 2


if __name__ == "__main__":
    raise SystemExit(principal())
