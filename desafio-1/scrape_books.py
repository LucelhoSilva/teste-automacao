"""Desafio 1 - Coleta os livros da categoria Mystery (books.toscrape.com).

author: Lucelho Silva

Usei httpx para baixar as paginas e BeautifulSoup para extrair os dados.
Salva o resultado em books.xlsx e mostra um resumo no terminal.
"""

from statistics import mean

import httpx
from bs4 import BeautifulSoup
from openpyxl import Workbook

URL_BASE = "https://books.toscrape.com"
URL_CATEGORIA = f"{URL_BASE}/catalogue/category/books/mystery_3/index.html"

# Converte o texto da classe CSS para o numero de estrelas.
ESTRELAS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def baixar_pagina(client, url):
    """Baixa uma pagina e devolve o objeto BeautifulSoup."""
    resposta = client.get(url)
    resposta.raise_for_status()
    return BeautifulSoup(resposta.text, "html.parser")


def ler_nota(book):
    """Le a nota em estrelas a partir da classe 'star-rating Three'."""
    classes = book.select_one("p.star-rating")["class"]
    palavra = [c for c in classes if c != "star-rating"][0]
    return ESTRELAS.get(palavra, 0)


def ler_detalhes(client, url_detalhe):
    """Bonus: entra na pagina do livro e pega a descricao e o UPC."""
    soup = baixar_pagina(client, url_detalhe)

    descricao_tag = soup.select_one("#product_description ~ p")
    descricao = descricao_tag.text.strip() if descricao_tag else ""

    upc = soup.select_one("table tr td").text.strip()
    return descricao, upc


def coletar_livros(client):
    """Percorre todas as paginas da categoria e devolve a lista de livros."""
    books = []
    url = URL_CATEGORIA

    while url:
        soup = baixar_pagina(client, url)

        for book in soup.select("article.product_pod"):
            link = book.select_one("h3 a")
            url_detalhe = f"{URL_BASE}/catalogue/{link['href'].replace('../../../', '')}"
            descricao, upc = ler_detalhes(client, url_detalhe)

            books.append({
                "titulo": link["title"],
                "preco": float(book.select_one("p.price_color").text.lstrip("£")),
                "nota": ler_nota(book),
                "disponibilidade": book.select_one("p.instock").text.strip(),
                "descricao": descricao,
                "upc": upc,
            })

        # Procura o link "next" para continuar a paginacao.
        proxima = soup.select_one("li.next a")
        if proxima:
            url = url.rsplit("/", 1)[0] + "/" + proxima["href"]
        else:
            url = None

    return books


def salvar_excel(books, arquivo="books.xlsx"):
    """Salva a lista de livros em uma planilha com cabecalho."""
    planilha = Workbook()
    aba = planilha.active
    aba.title = "Mystery"

    aba.append(["Titulo", "Preco (GBP)", "Nota", "Disponibilidade", "Descricao", "UPC"])
    for book in books:
        aba.append([
            book["titulo"],
            book["preco"],
            book["nota"],
            book["disponibilidade"],
            book["descricao"],
            book["upc"],
        ])

    planilha.save(arquivo)
    return arquivo


def mostrar_resumo(books):
    """Mostra o resumo pedido no terminal."""
    disponiveis = sum(1 for b in books if "In stock" in b["disponibilidade"])

    print("Total de livros:", len(books))
    print("Preco medio:", round(mean(b["preco"] for b in books), 2))
    print("Quantidade disponivel:", disponiveis)


def main():
    with httpx.Client(timeout=30) as client:
        books = coletar_livros(client)

    salvar_excel(books)
    print("Dados salvos em books.xlsx")
    mostrar_resumo(books)


if __name__ == "__main__":
    main()
