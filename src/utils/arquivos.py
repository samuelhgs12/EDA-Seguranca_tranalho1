from __future__ import annotations
from pathlib import Path

def ler_arquivo_texto(caminho: str | Path) -> str:
    return Path(caminho).read_text(encoding="utf-8")

def gravar_arquivo_texto(caminho: str | Path, conteudo: str) -> None:
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    Path(caminho).write_text(conteudo, encoding="utf-8")
