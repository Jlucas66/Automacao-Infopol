from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def configurar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def fazer_login(driver, wait, usuario, senha, url):
    print(f"🌍 Acessando: {url}")
    driver.get(url)
    
    try:
        # Tenta preencher automaticamente (usando os campos 'usr' e 'pwd' que mapeamos)
        wait.until(EC.presence_of_element_located((By.NAME, "usr"))).send_keys(usuario)
        driver.find_element(By.NAME, "pwd").send_keys(senha)
        print("⌨️ Dados de login preenchidos...")
        
        # O robô vai esperar você clicar em entrar ou resolver um captcha, se houver
        input("Pausa de Segurança: Faça o login manualmente no navegador e depois aperte ENTER aqui no terminal para continuar...")
        
    except Exception as e:
        print("⚠️ Não encontrei os campos de login. Você já está logado ou a URL mudou?")
        input("Ajuste a página manualmente e aperte ENTER aqui para prosseguir com o cadastro...")

def realizar_cadastro(driver, wait, dados):
    id_db, nome, cpf, data_nasc = dados
    print(f"📑 Iniciando preenchimento de: {nome}")
    
    # Aqui entrarão os IDs da página INTERNA do Infopol que você verá após o login
    # Exemplo genérico:
    # wait.until(EC.presence_of_element_located((By.ID, "campo_nome_interno"))).send_keys(nome)
    
    time.sleep(2) # Simula o tempo de preenchimento
    return True