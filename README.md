# EDA-Seguranca_trabalho1

Implementação do envelope digital assinado (AES-128-CBC + RSA + SHA-512).

## Requisitos

- Python 3.10+
- Dependências em `requirements.txt`

## Instalação

```bash
pip install -r requirements.txt
```

```powershell
pip install -r requirements.txt
```

## Uso (interface de linha de comando)

Execute a partir da raiz do projeto:

```bash
python src/principal.py --ajuda
```

```powershell
python src/principal.py --ajuda
```

### 1) Gerar par de chaves RSA (PEM)

```bash
python src/principal.py gerar-chaves --tamanho 2048 --privada-saida remetente_priv.pem --publica-saida remetente_pub.pem
```

```powershell
python src/principal.py gerar-chaves --tamanho 2048 --privada-saida remetente_priv.pem --publica-saida remetente_pub.pem
```

Arquivos gerados quando apenas o nome do arquivo é informado:

- `chaves/remetente_priv.pem`
- `chaves/remetente_pub.pem`

### 2) Criar envelope

Entrada: texto em claro, chave pública do destinatário e chave privada do remetente.
Saída: `.cif` (mensagem cifrada), `.env` (chave+IV cifrados) e `.sig` (assinatura).

```bash
python src/principal.py criar-envelope \
    --entrada mensagem.txt \
    --dest-publica chaves/destinatario_pub.pem \
    --remet-privada chaves/remetente_priv.pem \
    --diretorio-saida envelope \
    --nome-base envelope
```

```powershell
python src/principal.py criar-envelope `
    --entrada mensagem.txt `
    --dest-publica chaves/destinatario_pub.pem `
    --remet-privada chaves/remetente_priv.pem `
    --diretorio-saida envelope `
    --nome-base envelope
```

Arquivos gerados:

- `envelope/envelope.cif`
- `envelope/envelope.env`
- `envelope/envelope.sig`

### 3) Abrir envelope

Entrada: `.cif`, `.env`, `.sig`, chave privada do destinatário e chave pública do remetente.
Saída: arquivo em claro e status da assinatura.

```bash
python src/principal.py abrir-envelope \
    --cif envelope/envelope.cif \
    --env envelope/envelope.env \
    --sig envelope/envelope.sig \
    --dest-privada chaves/destinatario_priv.pem \
    --remet-publica chaves/remetente_pub.pem \
    --saida-claro mensagem_saida.txt
```

```powershell
python src/principal.py abrir-envelope `
    --cif envelope/envelope.cif `
    --env envelope/envelope.env `
    --sig envelope/envelope.sig `
    --dest-privada chaves/destinatario_priv.pem `
    --remet-publica chaves/remetente_pub.pem `
    --saida-claro mensagem_saida.txt
```

## Observações de formato

- AES-128-CBC com PKCS7.
- Assinatura RSA com SHA-512 (PKCS1v15).
- RSA para chave+IV: PKCS1v15.
- A chave e o IV (16 bytes cada) são concatenados em HEX e cifrados com RSA.
- Os arquivos `.cif`, `.env` e `.sig` são gravados em Base64.
- O texto em claro é tratado como UTF-8.
