# automation.py

import traceback
from app.db.database import buscar_codigo_unidade
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait

from app.automation.Funcoes_automacao import (
    clicar_alterar,
    clicar_gravar,
    fazer_login,
    navegar_para_usuarios,
    preencher_login,
    clicar_buscar,
    clicar_detalhar,
    detalhar_usuario,
    # alterar_unidade,
    limpar_checkboxes,
    logout,
    selecionar_unidade_por_codigo
)


def configurar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)


def executar_automacao(cpf, unidade_nome, usuario_infopol, senha_infopol):
    driver = configurar_driver()
    wait = WebDriverWait(driver, 15)

    try:
        print("🚀 Iniciando automação...")

        fazer_login(driver, wait, usuario_infopol, senha_infopol)

        navegar_para_usuarios(driver, wait)

        preencher_login(driver, wait, cpf)

        clicar_buscar(driver, wait)

        clicar_detalhar(driver, wait)

        detalhar_usuario(driver, wait)

        clicar_alterar(driver, wait)

        codigo = buscar_codigo_unidade(unidade_nome)

        if not codigo:
            raise Exception(f"Unidade '{unidade_nome}' não encontrada no banco de dados.")
        
        limpar_checkboxes(driver)

        selecionar_unidade_por_codigo(driver, wait, codigo)

        clicar_gravar(driver, wait)

        logout(driver, wait)

        print("✅ Automação concluída!")
        return True

    except Exception as e:
        print(f"❌ Erro na automação: {e}")
        print(type(e).__name__)
        print(str(e))
        traceback.print_exc()
        return False

    finally:
        print("🔒 Fechando navegador...")
        driver.quit()