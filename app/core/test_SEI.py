from selenium import webdriver

from app.core import config
from app.core.services.leitor_planilha import LeitorPlanilha

from app.automation.sei.login_SEI import LoginSei
from app.automation.sei.cadastro_usuario_SEI import CadastroUsuarioSei
from app.automation.sei.utils import gerar_sigla


CAMINHO = "app/data/AGENTES_NOVA_SENHA.xlsx"


def main():

    usuarios = LeitorPlanilha.carregar(
        caminho=CAMINHO,
        cargo="Agente"
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


    # =====================================
    # LOOP DA PLANILHA
    # =====================================
    for i, usuario in enumerate(usuarios):

        print(f"\n[{i+1}/{len(usuarios)}] Processando: {usuario.nome}")

        try:
            cadastro = CadastroUsuarioSei(driver)

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

            import traceback

            print("\n" + "=" * 80)
            print(f"[ERRO] Falha ao processar: {usuario.nome}")
            print(f"Tipo da exceção: {type(e).__name__}")
            print(f"Mensagem: {repr(e)}")
            print("\nTraceback completo:")
            traceback.print_exc()
            print("=" * 80 + "\n")

            # Fecha alerta, se existir
            try:
                driver.switch_to.alert.accept()
                print("[INFO] Alerta fechado.")
            except Exception:
                pass

            # Sai do iframe, se estiver dentro
            try:
                driver.switch_to.default_content()
                print("[INFO] Voltou para o conteúdo principal.")
            except Exception:
                pass

            # Fecha modal com ESC, se possível
            try:
                from selenium.webdriver.common.by import By
                from selenium.webdriver.common.keys import Keys

                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                print("[INFO] Modal fechado com ESC.")
            except Exception:
                pass

            # Recarrega a página para continuar o processamento
            try:
                driver.refresh()
                print("[INFO] Página recarregada.")
            except Exception:
                pass

            cadastro = CadastroUsuarioSei(driver)

            continue
    print("\nProcessamento finalizado.")


if __name__ == "__main__":
    main()