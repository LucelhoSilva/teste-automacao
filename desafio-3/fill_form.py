"""Desafio 3 - Preenchimento do formulario em demoqa.com/automation-practice-form.

Os dados vem do arquivo data.json. Ao final salva um screenshot do modal
de sucesso em confirmation.png.
"""

import json
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

URL_BASE = "https://demoqa.com/automation-practice-form"
PASTA = Path(__file__).parent


def carregar_dados():
    with open(PASTA / "data.json", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def preencher_formulario(pagina, dados):
    pagina.fill("#firstName", dados["nome"])
    pagina.fill("#lastName", dados["sobrenome"])
    pagina.fill("#userEmail", dados["email"])
    pagina.fill("#userNumber", dados["telefone"])

    # Genero e hobbies sao labels clicaveis (o input fica escondido).
    pagina.click(f"label:has-text('{dados['genero']}')")
    for hobby in dados["hobbies"]:
        pagina.click(f"//label[text()='{hobby}']")

    preencher_data_nascimento(pagina, dados["data_nascimento"])

    pagina.set_input_files("#uploadPicture", str(PASTA / dados["imagem"]))


def preencher_data_nascimento(pagina, data):
    pagina.click("#dateOfBirthInput")
    pagina.select_option(".react-datepicker__month-select", label=data["mes"])
    pagina.select_option(".react-datepicker__year-select", data["ano"])
    pagina.click(
        f".react-datepicker__day--{int(data['dia']):03d}"
        ":not(.react-datepicker__day--outside-month)"
    )


def enviar_e_validar(pagina, dados):
    # O botao de envio costuma ficar coberto por anuncios; o clique via JS evita isso.
    pagina.eval_on_selector("#submit", "el => el.click()")

    modal = pagina.locator(".modal-content")
    expect(modal).to_be_visible()
    expect(pagina.locator("#example-modal-sizes-title-lg")).to_have_text(
        "Thanks for submitting the form"
    )
    expect(modal).to_contain_text(f"{dados['nome']} {dados['sobrenome']}")

    modal.screenshot(path=str(PASTA / "confirmation.png"))
    print("Formulario enviado, screenshot salvo em confirmation.png")


def main():
    dados = carregar_dados()
    with sync_playwright() as playwright:
        navegador = playwright.chromium.launch(headless=True)
        pagina = navegador.new_page()

        pagina.goto(URL_BASE)
        preencher_formulario(pagina, dados)
        enviar_e_validar(pagina, dados)

        navegador.close()


if __name__ == "__main__":
    main()
