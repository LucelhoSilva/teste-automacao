"""Desafio 2 - Fluxo de login e compra no saucedemo.com.

As credenciais ficam listadas na propria pagina de login do site
(usuario "standard_user" e a senha mostrada em "Password for all users").
"""

from playwright.sync_api import expect, sync_playwright

URL_BASE = "https://www.saucedemo.com"
USUARIO = "standard_user"
SENHA = "secret_sauce"


def fazer_login(pagina):
    pagina.goto(URL_BASE)
    pagina.fill("#user-name", USUARIO)
    pagina.fill("#password", SENHA)
    pagina.click("#login-button")
    # Confirma que o login deu certo chegando no catalogo.
    expect(pagina).to_have_url(f"{URL_BASE}/inventory.html")


def filtrar_preco_menor_para_maior(pagina):
    pagina.select_option(".product_sort_container", "lohi")


def adicionar_tres_produtos(pagina):
    botoes = pagina.locator("button:has-text('Add to cart')")
    # Apos o clique o botao vira "Remove", entao sempre pego o primeiro disponivel.
    for _ in range(3):
        botoes.nth(0).click()
    expect(pagina.locator(".shopping_cart_badge")).to_have_text("3")


def fazer_checkout(pagina):
    pagina.click(".shopping_cart_link")
    pagina.click("#checkout")

    pagina.fill("#first-name", "Lucelho")
    pagina.fill("#last-name", "Silva")
    pagina.fill("#postal-code", "12345")
    pagina.click("#continue")

    pagina.click("#finish")
    expect(pagina.locator(".complete-header")).to_have_text("Thank you for your order!")


def fazer_logout(pagina):
    pagina.click("#react-burger-menu-btn")
    pagina.click("#logout_sidebar_link")
    # Confirma que voltou para a tela de login.
    expect(pagina.locator("#login-button")).to_be_visible()


def main():
    with sync_playwright() as playwright:
        navegador = playwright.chromium.launch(headless=True)
        pagina = navegador.new_page()

        fazer_login(pagina)
        filtrar_preco_menor_para_maior(pagina)
        adicionar_tres_produtos(pagina)
        fazer_checkout(pagina)
        fazer_logout(pagina)

        print("Fluxo concluido com sucesso")
        navegador.close()


if __name__ == "__main__":
    main()
