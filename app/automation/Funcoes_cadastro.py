import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

load_dotenv()

#clica na parte para selecionar 'usuário' e abrir a tela base de usuários.
def selecionar_tabela_usuarios(driver, wait):
    print("📋 Selecionando 'Usuários'...")

    select_element = wait.until(
        EC.presence_of_element_located((By.NAME, "tabela"))
    )

    select = Select(select_element)
    select.select_by_visible_text("Usuários")

# clica no botão 'exibir' para seguir para a tela base de usuários.
def clicar_exibir(driver, wait):
    print("👁️ Clicando no botão 'Exibir'...")

    botao = wait.until(
        EC.element_to_be_clickable((By.ID, "botao_exibir"))
    )

    botao.click()


# Navegar até a tela base de usuários
def navegar_para_usuarios(driver, wait):
    print("📂 Navegando até usuários...")

    try:
        menu = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'UTILITARIOS')]"))
        )
        ActionChains(driver).move_to_element(menu).perform()

    except:
        menus = driver.find_elements(By.XPATH, "//nav//a | //nav//span")
        if menus:
            ActionChains(driver).move_to_element(menus[0]).perform()
        else:
            raise Exception("Menu principal não encontrado.")

    adm = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Adm de Usuarios')]"))
    )
    adm.click()

    relatorio = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Manutenção de Usuários')]"))
    )
    relatorio.click()

    selecionar_tabela_usuarios(driver, wait)
    clicar_exibir(driver, wait)

    print("✅ Tela de busca carregada!")

#clica no botão "novo" para seguir para cadastro de novo usuário.
def clicar_novo(driver, wait):
    print("👁️ Clicando no botão 'Novo'...")

    botao = wait.until(
        EC.element_to_be_clickable((By.ID, "botao_incluir"))
    )

    botao.click()    




# 🚪 Logout
def logout(driver, wait):
    print("🚪 Realizando logout...")

    try:
        botao_logout = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Sair')]"))
        )
        botao_logout.click()
    except Exception:
        print("⚠️ Botão de logout não encontrado.")
