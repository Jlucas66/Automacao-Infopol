# automation.py

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from Funcoes_automacao import (
    clicar_alterar,
    fazer_login,
    navegar_para_usuarios,
    preencher_login,
    clicar_buscar,
    clicar_detalhar,
    detalhar_usuario,
    alterar_unidade,
    logout
)


def configurar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)


def executar_automacao(cpf, unidade_nome):
    driver = configurar_driver()
    wait = WebDriverWait(driver, 15)

    try:
        print("🚀 Iniciando automação...")

        fazer_login(driver, wait)

        navegar_para_usuarios(driver, wait)

        preencher_login(driver, wait, cpf)

        clicar_buscar(driver, wait)

        clicar_detalhar(driver, wait)

        detalhar_usuario(driver, wait)

        clicar_alterar(driver, wait)

        alterar_unidade(driver, wait, unidade_nome)

        logout(driver, wait)

        print("✅ Automação concluída!")
        return True

    except Exception as e:
        print(f"❌ Erro na automação: {e}")
        return False

    finally:
        print("🔒 Fechando navegador...")
        driver.quit()