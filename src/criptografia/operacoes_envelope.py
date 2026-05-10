from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from criptografia.operacoes_aes import (
    cifrar_aes_cbc_pkcs7,
    decifrar_aes_cbc_pkcs7,
    gerar_chave_iv_aes128,
)
from criptografia.operacoes_assinatura import assinar_sha512_rsa, verificar_sha512_rsa
from criptografia.operacoes_rsa import cifrar_rsa_pkcs1v15, decifrar_rsa_pkcs1v15
from utils.arquivos import gravar_arquivo_texto, ler_arquivo_texto
from utils.codificacao import (
    de_base64,
    desempacotar_chave_iv_hex,
    empacotar_chave_iv_hex,
    para_base64,
)
from utils.validadores import garantir_extensao_envelope_suportada


@dataclass(frozen=True)
class ArtefatosEnvelope:
    mensagem_cifrada: Path
    sessao_cifrada: Path
    assinatura: Path


def criar_caminhos_envelope(
    nome_base: str, diretorio_saida: str | Path = "envelope"
) -> ArtefatosEnvelope:
    raiz = Path(diretorio_saida)
    return ArtefatosEnvelope(
        mensagem_cifrada=raiz / f"{nome_base}.cif",
        sessao_cifrada=raiz / f"{nome_base}.env",
        assinatura=raiz / f"{nome_base}.sig",
    )


def validar_caminhos_artefatos(artefatos: ArtefatosEnvelope) -> None:
    garantir_extensao_envelope_suportada(artefatos.mensagem_cifrada, ".cif")
    garantir_extensao_envelope_suportada(artefatos.sessao_cifrada, ".env")
    garantir_extensao_envelope_suportada(artefatos.assinatura, ".sig")


def criar_envelope(
    caminho_texto_claro: str | Path,
    chave_publica_destinatario,
    chave_privada_remetente,
    artefatos: ArtefatosEnvelope,
) -> None:
    validar_caminhos_artefatos(artefatos)
    texto_claro = ler_arquivo_texto(caminho_texto_claro).encode("utf-8")
    chave, iv = gerar_chave_iv_aes128()

    texto_cifrado = cifrar_aes_cbc_pkcs7(texto_claro, chave, iv)
    hex_empacotado = empacotar_chave_iv_hex(chave, iv)
    sessao_cifrada = cifrar_rsa_pkcs1v15(
        hex_empacotado.encode("ascii"), chave_publica_destinatario
    )
    assinatura = assinar_sha512_rsa(texto_claro, chave_privada_remetente)

    gravar_arquivo_texto(artefatos.mensagem_cifrada, para_base64(texto_cifrado))
    gravar_arquivo_texto(artefatos.sessao_cifrada, para_base64(sessao_cifrada))
    gravar_arquivo_texto(artefatos.assinatura, para_base64(assinatura))


def abrir_envelope(
    artefatos: ArtefatosEnvelope,
    chave_privada_destinatario,
    chave_publica_remetente,
) -> tuple[str, bool, str, str]:
    validar_caminhos_artefatos(artefatos)

    texto_cifrado = de_base64(ler_arquivo_texto(artefatos.mensagem_cifrada).strip())
    sessao_cifrada = de_base64(ler_arquivo_texto(artefatos.sessao_cifrada).strip())
    assinatura = de_base64(ler_arquivo_texto(artefatos.assinatura).strip())

    hex_empacotado = decifrar_rsa_pkcs1v15(
        sessao_cifrada, chave_privada_destinatario
    ).decode("ascii")
    chave, iv = desempacotar_chave_iv_hex(hex_empacotado)

    texto_claro = decifrar_aes_cbc_pkcs7(texto_cifrado, chave, iv)
    assinatura_valida = verificar_sha512_rsa(texto_claro, assinatura, chave_publica_remetente)

    return texto_claro.decode("utf-8"), assinatura_valida, chave.hex(), iv.hex()
