# import os
# import traceback
# # from db.database import buscar_codigo_unidade
# from selenium import webdriver
# import time
# from selenium.webdriver.support.ui import WebDriverWait


# from app.automation.Funcoes_cadastro import (
#     selecionar_tabela_usuarios,
#     clicar_exibir,
#     navegar_para_usuarios,
#     clicar_novo,
#     fazer_login,
#     logout 
# )

# def configurar_driver():
#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")
#     return webdriver.Chrome(options=options)

# def executar_automacao(usuario_infopol, senha_infopol):
#     driver = configurar_driver()
#     wait = WebDriverWait(driver, 15)

#     try:
#         print("🚀 Iniciando automação...")

#         fazer_login(driver, wait, usuario_infopol, senha_infopol)

#         navegar_para_usuarios(driver, wait)

#         selecionar_tabela_usuarios(driver, wait)

#         # clicar_exibir(driver, wait)

#         clicar_novo(driver, wait)

#         logout(driver, wait)

#         print("✅ Automação concluída!")
#         return True

#     except Exception as e:
#         print(f"❌ Erro na automação: {e}")
#         print(type(e).__name__)
#         print(str(e))
#         traceback.print_exc()
#         return False

#     finally:
#         print("🔒 Fechando navegador...")
#         driver.quit()

# if __name__ == "__main__":

#     executar_automacao(
#         usuario_infopol = os.getenv("INFOPOL_USER"),
#         senha_infopol = os.getenv("INFOPOL_PASS")
#     )

#     print("teste de cadastro concluído!")     
from app.core.services.consolidar_planilhas import (
    ConsolidadorPlanilhas
)

CAMINHO_ACADEPOL = (
    "app/data/ACADEPOL Delegados 14-06.xlsx"
)

CAMINHO_COMPLETA = (
    "app/data/tabela-completa.xlsx"
)

df = ConsolidadorPlanilhas.consolidar(
    CAMINHO_ACADEPOL,
    CAMINHO_COMPLETA
)

print("\nColunas encontradas:\n")
print(df.columns.tolist())

print("\nPrimeiros registros:\n")

colunas = [
    "nome_pessoa",
    "cpf corrigido",
    "email",
    "sexo",
    "matricula_nova",
    "data_admissao",
]

print(df[colunas].head(20))