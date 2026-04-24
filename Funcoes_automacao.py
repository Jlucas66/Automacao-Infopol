# funcoes_automacao.py

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


def selecionar_tabela_usuarios(driver, wait):
    print("📋 Selecionando 'Usuários'...")

    select_element = wait.until(
        EC.presence_of_element_located((By.NAME, "tabela"))
    )

    select = Select(select_element)
    select.select_by_visible_text("Usuários")


def fazer_login(driver, wait):
    url = os.getenv("INFOPOL_URL")
    usuario = os.getenv("INFOPOL_USER")
    senha = os.getenv("INFOPOL_PASSWORD")

    print(f"🌍 Acessando: {url}")
    driver.get(url)

    try:
        wait.until(EC.presence_of_element_located((By.NAME, "usr"))).send_keys(usuario)
        driver.find_element(By.NAME, "pwd").send_keys(senha)

        print("⌨️ Dados preenchidos.")

        input("👉 Faça login manual (captcha/se necessário) e pressione ENTER...")

    except:
        print("⚠️ Login manual necessário.")
        input("👉 Faça login e pressione ENTER...")

    # 🔥 GARANTE QUE O SISTEMA CARREGOU
    print("⏳ Aguardando sistema carregar...")

    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # 👇 DEBUG: veja se carregou algo útil
    print("✅ Página carregada!")  


# 📂 Navegar até a tela de usuários
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
  

def clicar_exibir(driver, wait):
    print("👁️ Clicando no botão 'Exibir'...")

    botao = wait.until(
        EC.element_to_be_clickable((By.ID, "botao_exibir"))
    )

    botao.click()


def preencher_login(driver, wait, cpf):
    print("👉 Preenchendo campo login...")

    campo = wait.until(
        EC.element_to_be_clickable((By.ID, "login"))
    )

    campo.clear()
    campo.send_keys(cpf)

    # 🔥 ESSENCIAL: dispara evento do sistema
    campo.send_keys(Keys.TAB)

    print("✅ CPF preenchido!")

def clicar_buscar(driver, wait):
    import time
    print("🔎 Clicando em Buscar...")

    botao = wait.until(
        EC.presence_of_element_located((By.ID, "botao_buscar"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", botao)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", botao)

    print("⏳ Aguardando resultado...")

    # 🔥 Espera pela TABELA de resultados, não pelo texto "Detalhar"
    # A linha do resultado tem class="tabelaLinhaPar"
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "tabelaLinhaPar"))
    )

    print("✅ Busca realizada!")

def clicar_detalhar(driver, wait):
    import time, re
    print("👤 Clicando em Detalhar...")

    # Pega o ID do usuário do link
    link = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href,'detalhar')]")
        )
    )
    href = link.get_attribute("href")
    print(f"🔗 href: {href}")

    match = re.search(r"id=(\d+)", href)
    if not match:
        raise Exception("ID do usuário não encontrado no href")
    
    user_id = match.group(1)
    print(f"🆔 ID: {user_id}")

    # 🔥 USA callPage DIRETO — igual ao que o sistema usa internamente
    # A URL real é /pernambuco/usuario.do?acao=detalhar&id=XXXX
    driver.execute_script(
        f"callPage('/usuario.do?acao=detalhar&id={user_id}');"
    )
    print("⏳ Aguardando AJAX da tela de detalhe...")

    # Aguarda o conteúdo mudar — espera o divConteudoHtml ter "bto_alterar"
    # que é o botão Alterar da tela de detalhe
    wait.until(
        lambda d: "bto_alterar" in d.find_element(
            By.ID, "divConteudoHtml"
        ).get_attribute("innerHTML")
    )

    print("✅ Tela de detalhe carregada!")
    return True

def clicar_alterar(driver, wait):
    print("✏️ Clicando no botão Alterar...")

    botao = wait.until(
        EC.presence_of_element_located((By.ID, "botao_alterar"))
    )

    # scroll até o botão
    driver.execute_script("arguments[0].scrollIntoView(true);", botao)

    import time
    time.sleep(1)

    # clique via JS (mesmo padrão que funcionou antes)
    driver.execute_script("arguments[0].click();", botao)

    print("✅ Clique em Alterar realizado!")

    # espera a próxima tela carregar
    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

# 🔎 Buscar CPF
def buscar_usuario(driver, wait, cpf):
    print(f"🔎 Buscando CPF: {cpf}")

    campo_cpf = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'CPF')]"))
    )
    campo_cpf.clear()
    campo_cpf.send_keys(cpf)

    botao_buscar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Buscar')]"))
    )
    botao_buscar.click()


# 👤 Detalhar usuário
def detalhar_usuario(driver, wait):
    print("👤 Verificando tela de detalhe...")
    # Só confirma que está na tela certa — o clique já foi feito em clicar_detalhar
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("✅ Na tela de detalhe!")


def limpar_checkboxes(driver):
    print("🧹 Limpando checkboxes...")

    checkboxes = driver.find_elements(By.NAME, "chkListaUnidadeOperacional")

    for cb in checkboxes:
        if cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)

    print("✅ Limpo!")


def selecionar_unidade_por_codigo(driver, wait, codigo):
    print(f"🎯 Selecionando unidade código: {codigo}")

    import time

    # 🔎 tenta encontrar checkbox pelo value
    xpath = f"//input[@type='checkbox' and @value='{codigo}']"

    checkbox = wait.until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

    # rola até ele
    driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
    time.sleep(0.5)

    # marca via JS (mais confiável que click)
    driver.execute_script("arguments[0].checked = true;", checkbox)

    print("✅ Unidade marcada!")


def clicar_gravar(driver, wait):
    print("💾 Clicando em Gravar...")

    botao = wait.until(
        EC.presence_of_element_located((By.ID, "botao_gravar"))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", botao)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", botao)

    print("✅ Alteração salva!")


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

