from selenium import webdriver

from app.automation.sip.login import LoginSip
from app.automation.sip.cadastro_usuario import CadastroUsuario
from app.automation.sip.permissao_usuario import PermissaoUsuario
from app.automation.sip.utils import gerar_sigla

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

    usuarios = LeitorPlanilha.carregar(
        caminho,
        cargo="Delegado"
    )

    delegado = usuarios[0]

    print()
    print("Primeiro delegado:")
    print(delegado)
    print("Matrícula:", delegado.matricula)
    print("Sexo:", delegado.sexo)
    print()

    driver = webdriver.Chrome()

    driver.maximize_window()

    driver.get(SIP_URL)

    LoginSip(driver).realizar_login(
        SIP_USUARIO,
        SIP_SENHA
    )

    # ==========================
    # Cadastro do usuário
    # ==========================
    cadastro = CadastroUsuario(driver)

    cadastro.abrir_tela_novo_usuario()

    cadastro.preencher(delegado)

    # input(
    #     "\nConfira os dados do cadastro e pressione ENTER para salvar."
    # )

    cadastro.salvar()

    # ==========================
    # Permissão no SEI
    # ==========================
    permissao = PermissaoUsuario(driver)

    permissao.abrir_permissoes()

    permissao.abrir_nova_permissao()

    permissao.preencher(
        gerar_sigla(delegado.email)
    )

    permissao.salvar()

    driver.quit()


if __name__ == "__main__":
    main()