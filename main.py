import os
import time
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
import database as db
import automation as auto

load_dotenv()

def executar_robo():
    print("🚀 Iniciando Automação Infopol...")
    
    # 1. Busca dados no Postgres
    registros = db.buscar_registros_pendentes()
    if not registros:
        print("Putz! Nada para cadastrar no momento. Encerrando...")
        return

    # 2. Inicia o Navegador
    driver = auto.configurar_driver()
    wait = WebDriverWait(driver, 15)

    try:
        # 3. Login
        auto.fazer_login(
            driver, wait, 
            os.getenv("INFOPOL_USER"), 
            os.getenv("INFOPOL_PASS"), 
            os.getenv("INFOPOL_URL")
        )
        print("🔑 Login efetuado com sucesso!")

        # 4. Loop de Cadastro
        for pessoa in registros:
            id_atual = pessoa[0]
            nome_atual = pessoa[1]
            
            try:
                print(f"📝 Cadastrando: {nome_atual}...")
                sucesso = auto.realizar_cadastro(driver, wait, pessoa)
                
                if sucesso:
                    db.atualizar_status_no_banco(id_atual, 'concluido')
                    print(f"✅ {nome_atual} finalizado!")
                
                time.sleep(10) # Pausa humana
                
            except Exception as e:
                print(f"⚠️ Erro ao cadastrar {nome_atual}: {e}")
                db.atualizar_status_no_banco(id_atual, 'erro')

    except Exception as e:
        print(f"❌ Erro crítico no sistema: {e}")
    
    finally:
        print("🏁 Fim do processo. Fechando navegador...")
        driver.quit()

if __name__ == "__main__":
    executar_robo()