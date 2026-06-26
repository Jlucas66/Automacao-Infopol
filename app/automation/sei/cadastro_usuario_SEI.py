import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CadastroUsuarioSei:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # =====================================================
    # MENU
    # =====================================================
    def abrir_listar_usuarios(self):

        self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "linkMenu1")
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "linkMenu19")
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "linkMenu20")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "txtSiglaUsuario")
            )
        )

    # =====================================================
    # PESQUISAR USUÁRIO
    # =====================================================
    def pesquisar_usuario(self, sigla):

        campo = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "txtSiglaUsuario")
            )
        )

        campo.clear()
        campo.send_keys(sigla)

        self.driver.find_element(
            By.ID,
            "btnPesquisar"
        ).click()

        alterar = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//img[@title='Alterar Usuário']"
                )
            )
        )

        alterar.click()

    # =====================================================
    # ABRIR BOX DO CONTATO
    # =====================================================
    def abrir_alterar_contato(self):

        self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "imgAlterarContato")
            )
        ).click()

        time.sleep(2)

    # =====================================================
    # PREENCHER DADOS
    # =====================================================
    def preencher(self, usuario):

        # -------------------------
        # SEXO
        # -------------------------
        if usuario.sexo and usuario.sexo.upper() == "F":

            self.wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "lblFeminino")
                )
            ).click()

        else:

            self.wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "lblMasculino")
                )
            ).click()   

        # -------------------------
        # CARGO
        # -------------------------

        cargo_usuario = usuario.cargo.upper()

        if "DELEGADO" in cargo_usuario:

            cargo_sei = "Delegado de Polícia Civil"

        elif "ESCRIV" in cargo_usuario:

            cargo_sei = "Escrivão de Polícia"

        elif "AGENTE" in cargo_usuario:

            cargo_sei = "Agente de Polícia"

        else:

            raise Exception(
                f"Cargo não reconhecido: {usuario.cargo}"
            )

        select_cargo = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "selCargo")
            )
        )

        Select(select_cargo).select_by_visible_text(
            cargo_sei
        )

        time.sleep(2)

    # =====================================================
    # SALVAR
    # =====================================================
    def salvar(self):

        url_antes = self.driver.current_url

        # Salvar box de contato
        botao_salvar1 = self.wait.until(
            EC.element_to_be_clickable(
                (By.NAME, "sbmAlterarContato")
            )
        )

        botao_salvar1.click()

        time.sleep(2)

        # Verifica se apareceu algum Alert
        try:

            alert = Alert(self.driver)

            mensagem = alert.text

            alert.accept()

            raise Exception(
                f"[ERRO] Sistema retornou: {mensagem}"
            )

        except:

            pass

        # Salvar usuário
        botao_salvar2 = self.wait.until(
            EC.element_to_be_clickable(
                (By.NAME, "sbmAlterarUsuario")
            )
        )

        botao_salvar2.click()

        try:

            self.wait.until(
                EC.url_changes(url_antes)
            )

            print("[OK] Cadastro no SEI finalizado.")

        except:

            self.driver.save_screenshot(
                "erro_salvar_sei.png"
            )

            raise Exception(
                "Salvar não foi confirmado. Screenshot salva como erro_salvar_sei.png"
            )