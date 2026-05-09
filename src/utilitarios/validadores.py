from __future__ import annotations

from pathlib import Path


EXTENSAO_BIN_LEGADA = ".bin"


def garantir_extensao_envelope_suportada(caminho: str | Path, sufixo_esperado: str) -> None:
    sufixo = Path(caminho).suffix.lower()
    if sufixo != sufixo_esperado.lower():
        dica = ""
        if sufixo == EXTENSAO_BIN_LEGADA:
            dica = f" A extensão legada '.bin' não é aceita; renomeie/use '{sufixo_esperado}'."
        raise ValueError(
            f"Extensão inválida '{sufixo}' para '{caminho}'. Esperado: '{sufixo_esperado}'.{dica}"
        )
