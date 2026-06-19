# Teste técnico — Dev Python (Automação)

Três automações em Python 3.10+, uma por desafio:

| Pasta | Site | Ferramenta | O que faz |
|-------|------|------------|-----------|
| `desafio-1/` | books.toscrape.com | **httpx** + BeautifulSoup | Coleta os livros da categoria *Mystery*, salva em `books.xlsx` e mostra um resumo |
| `desafio-2/` | saucedemo.com | **Playwright** | Login, filtro de preço, carrinho, checkout e logout |
| `desafio-3/` | demoqa.com | **Playwright** | Preenche e envia o formulário a partir de `data.json` e salva `confirmation.png` |

## Pré-requisitos

- Python 3.10 ou superior
- Cada desafio tem seu próprio `requirements.txt`

Recomendo um ambiente virtual:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

---

## Desafio 1 — Scraping de e-commerce (httpx)

```bash
cd desafio-1
pip install -r requirements.txt
python scrape_books.py
```

Gera o `books.xlsx` (título, preço, nota, disponibilidade, descrição e UPC) e imprime
o total de livros, o preço médio e a quantidade disponível.

## Desafio 2 — Login e checkout (Playwright)

```bash
cd desafio-2
pip install -r requirements.txt
python -m playwright install chromium
python login_flow.py
```

> As credenciais ficam listadas na própria tela de login do saucedemo
> (`standard_user` / `secret_sauce`).

## Desafio 3 — Formulário com validações (Playwright)

```bash
cd desafio-3
pip install -r requirements.txt
python -m playwright install chromium
python fill_form.py
```

Os dados de preenchimento vêm de `data.json`. Ao final é gerado o `confirmation.png`
com o modal de sucesso.

---

## Bônus — Docker

Cada desafio tem um `Dockerfile` que roda a automação em modo headless. Os arquivos
de saída são montados via volume para ficarem acessíveis fora do container.

**Desafio 1** (gera `books.xlsx` na pasta atual):

```bash
cd desafio-1
docker build -t teste-desafio-1 .
docker run --rm -v "$(pwd):/app" teste-desafio-1
```

**Desafio 2** (apenas executa o fluxo e imprime o resultado):

```bash
cd desafio-2
docker build -t teste-desafio-2 .
docker run --rm teste-desafio-2
```

**Desafio 3** (gera `confirmation.png` na pasta atual):

```bash
cd desafio-3
docker build -t teste-desafio-3 .
docker run --rm -v "$(pwd):/app" teste-desafio-3
```

> No Windows (PowerShell), troque `$(pwd)` por `${PWD}`.
