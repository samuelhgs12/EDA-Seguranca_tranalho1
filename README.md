# EDA-Seguranca_trabalho1

Implementacao do envelope digital assinado (AES-128-CBC + RSA + SHA-512).

## Requisitos

- Python 3.10+
- Dependencias em `requirements.txt`

## Instalacao

```bash
pip install -r requirements.txt
```

```powershell
pip install -r requirements.txt
```

## Uso (CLI)

Execute a partir da raiz do projeto:

```bash
python src/main.py --help
```

```powershell
python src/main.py --help
```

### 1) Gerar par de chaves RSA (PEM)

```bash
python src/main.py gen-keys --bits 2048 --private-out sender_priv.pem --public-out sender_pub.pem
```

```powershell
python src/main.py gen-keys --bits 2048 --private-out sender_priv.pem --public-out sender_pub.pem
```

Arquivos gerados (por padrao):

- `keys/sender_priv.pem`
- `keys/sender_pub.pem`

### 2) Criar envelope (seal)

Entrada: texto em claro, chave publica do destinatario, chave privada do remetente.
Saida: `.cif` (mensagem cifrada), `.env` (chave+IV cifrados), `.sig` (assinatura).

```bash
python src/main.py seal \
	--in mensagem.txt \
	--dest-pub keys/dest_pub.pem \
	--sender-priv keys/sender_priv.pem \
	--out-dir envelope \
	--base-name envelope
```

```powershell
python src/main.py seal `
    --in mensagem.txt `
    --dest-pub keys/dest_pub.pem `
    --sender-priv keys/sender_priv.pem `
    --out-dir envelope `
    --base-name envelope
```

Arquivos gerados:

- `envelope/envelope.cif`
- `envelope/envelope.env`
- `envelope/envelope.sig`

### 3) Abrir envelope (open)

Entrada: `.cif`, `.env`, `.sig`, chave privada do destinatario, chave publica do remetente.
Saida: arquivo em claro e status da assinatura.

```bash
python src/main.py open \
	--cif envelope/envelope.cif \
	--env envelope/envelope.env \
	--sig envelope/envelope.sig \
	--dest-priv keys/dest_priv.pem \
	--sender-pub keys/sender_pub.pem \
	--out-plain mensagem_out.txt
```

```powershell
python src/main.py open `
    --cif envelope/envelope.cif `
    --env envelope/envelope.env `
    --sig envelope/envelope.sig `
    --dest-priv keys/dest_priv.pem `
    --sender-pub keys/sender_pub.pem `
    --out-plain mensagem_out.txt
```

## Observacoes de formato

- AES-128-CBC com PKCS7.
- Assinatura RSA com SHA-512 (PKCS1v15).
- RSA para chave+IV: PKCS1v15.
- A chave e o IV (16 bytes cada) sao concatenados em HEX e cifrados com RSA.
- Os arquivos `.cif`, `.env` e `.sig` sao gravados em Base64.
- O texto em claro e tratado como UTF-8.