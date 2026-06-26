from selenium import webdriver

from app.core import config
from app.core.services.leitor_planilha import LeitorPlanilha

from app.automation.sei.login_SEI import LoginSei
from app.automation.sei.cadastro_usuario_SEI import CadastroUsuarioSei
from app.automation.sei.utils import gerar_sigla


CAMINHO = "app/data/ACADEPOL Delegados 14-06.xlsx"


def main():

    usuarios = LeitorPlanilha.carregar(
        caminho=CAMINHO,
        cargo="Delegado"
    )

    if not usuarios:
        print("Nenhum usuário encontrado.")
        return

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

    cadastro = CadastroUsuarioSei(driver)

    # =====================================
    # LOOP DA PLANILHA
    # =====================================
    for i, usuario in enumerate(usuarios):

        print(f"\n[{i+1}/{len(usuarios)}] Processando: {usuario.nome}")

        try:

            # Sempre volta para a tela de pesquisa
            cadastro.abrir_listar_usuarios()

            cadastro.pesquisar_usuario(
                gerar_sigla(usuario.email)
            )

            cadastro.abrir_alterar_contato()

            cadastro.preencher(usuario)

            cadastro.salvar()

            print(f"[OK] {usuario.nome} atualizado com sucesso.")

        except Exception as e:

            print(f"[ERRO] {usuario.nome}: {e}")

            # Fecha eventual alerta do SEI
            try:
                driver.switch_to.alert.accept()
            except Exception:
                pass

            continue

    driver.quit()

    print("\nProcessamento finalizado.")


if __name__ == "__main__":
    main()