from selenium import webdriver

from app.automation.sip.login import LoginSip
from app.automation.sip.cadastro_usuario import CadastroUsuario

from app.core.config import (
    SIP_URL,
    SIP_USUARIO,
    SIP_SENHA
)

from app.core.services.leitor_planilha import (
    LeitorPlanilha
)

caminho = "app/data/ACADEPOL Delegados 14-06.xlsx"


def main():

    usuarios = LeitorPlanilha.carregar(caminho)

    delegado = usuarios[0]

    print()
    print("Primeiro delegado:")
    print(delegado)
    print()

    driver = webdriver.Chrome()

    driver.maximize_window()

    driver.get(SIP_URL)

    LoginSip(driver).realizar_login(
        SIP_USUARIO,
        SIP_SENHA
    )

    cadastro = CadastroUsuario(driver)

    cadastro.abrir_tela_novo_usuario()

    cadastro.preencher(delegado)

    input(
        "\nConfira os dados preenchidos e pressione ENTER."
    )

    driver.quit()


if __name__ == "__main__":
    main()