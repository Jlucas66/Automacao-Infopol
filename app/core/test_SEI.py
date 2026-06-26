from selenium import webdriver

from app.core import config
from app.core.services.leitor_planilha import LeitorPlanilha
from app.automation.sei.utils import gerar_sigla

from app.automation.sei.login_SEI import LoginSei
from app.automation.sei.cadastro_usuario_SEI import CadastroUsuarioSei


def main():

    driver = webdriver.Chrome()

    driver.maximize_window()

    driver.get(config.SEI_URL)

    # =====================================
    # LOGIN
    # =====================================
    login = LoginSei(driver)

    login.realizar_login(
        usuario=config.SIP_USUARIO,
        senha=config.SIP_SENHA
    )

    # =====================================
    # CARREGA APENAS A PLANILHA DE DELEGADOS
    # =====================================
    caminho = "app/data/ACADEPOL Delegados 14-06.xlsx"

    usuarios = LeitorPlanilha.carregar(
        caminho=caminho,
        cargo="Delegado"
    )

    if not usuarios:
        print("Nenhum usuário encontrado.")
        driver.quit()
        return

    # Apenas o primeiro usuário
    usuario = usuarios[0]

    print(f"Testando usuário: {usuario.nome}")

    cadastro = CadastroUsuarioSei(driver)

    cadastro.abrir_listar_usuarios()

    cadastro.pesquisar_usuario(
        gerar_sigla(usuario.email)
    )

    cadastro.abrir_alterar_contato()

    print(usuario.nome)
    print("Sexo:", usuario.sexo)
    print("Cargo:", usuario.cargo)
    print("Email:", usuario.email)

    cadastro.preencher(usuario)

    cadastro.salvar()

    print(f"[OK] Cadastro realizado para {usuario.nome}")

    input("Pressione ENTER para fechar...")

    driver.quit()


if __name__ == "__main__":
    main()