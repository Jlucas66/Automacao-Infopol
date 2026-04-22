# funcoes_automacao.py

import os
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


def alterar_unidade(driver, wait, unidade_nome):
    print(f"🏢 Alterando unidade para: {unidade_nome}")
    import time

    # Botão Alterar pode ser <input type="submit"> em sistemas legados
    estrategias_alterar = [
        (By.XPATH, "//input[@value='Alterar']"),
        (By.XPATH, "//button[contains(text(),'Alterar')]"),
        (By.XPATH, "//*[contains(@onclick,'alterar')]"),
    ]
    for est in estrategias_alterar:
        els = driver.find_elements(*est)
        if els:
            driver.execute_script("arguments[0].click();", els[0])
            print("✅ Clicou em Alterar")
            break

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)

    # Unidade pode ser <select>, <radio>, ou <label> — tenta as três
    try:
        select_el = driver.find_element(By.XPATH, "//select[contains(@name,'unidade') or contains(@id,'unidade')]")
        Select(select_el).select_by_visible_text(unidade_nome)
        print("✅ Unidade selecionada via <select>")
    except Exception:
        try:
            label = driver.find_element(By.XPATH, f"//label[contains(text(),'{unidade_nome}')]")
            driver.execute_script("arguments[0].click();", label)
            print("✅ Unidade selecionada via <label>")
        except Exception:
            radio = driver.find_element(By.XPATH, f"//input[@type='radio'][following-sibling::*[contains(text(),'{unidade_nome}')] or @value='{unidade_nome}']")
            driver.execute_script("arguments[0].click();", radio)
            print("✅ Unidade selecionada via radio button")

    # Gravar
    estrategias_gravar = [
        (By.XPATH, "//input[@value='Gravar']"),
        (By.XPATH, "//button[contains(text(),'Gravar')]"),
    ]
    for est in estrategias_gravar:
        els = driver.find_elements(*est)
        if els:
            driver.execute_script("arguments[0].click();", els[0])
            print("✅ Gravado!")
            break


# 🏢 Alterar unidade
def alterar_unidade(driver, wait, unidade_nome):
    print(f"🏢 Alterando unidade para: {unidade_nome}")

    # 7. Clicar em Alterar
    botao_alterar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Alterar')]"))
    )
    botao_alterar.click()

    # 8. Espera tela carregar
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 9. Selecionar unidade (ajustar conforme HTML real)
    unidade = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//label[contains(text(), '{unidade_nome}')]"))
    )
    unidade.click()

    # 10. Gravar
    botao_gravar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Gravar')]"))
    )
    botao_gravar.click()


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

