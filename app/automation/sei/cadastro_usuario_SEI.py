import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException


class CadastroUsuarioSei:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # =====================================================
    # MENU
    # =====================================================
    def abrir_listar_usuarios(self):

    # Sempre começa da página principal
            self.driver.switch_to.default_content()

            # Fecha alerta pendente, se existir
            try:
                Alert(self.driver).accept()
                time.sleep(1)
            except:
                pass

            # Se já estiver na tela de pesquisa, não navega novamente
            if self.driver.find_elements(By.ID, "txtSiglaUsuario"):
                return

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

        self.driver.switch_to.default_content()

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

        # Espera a pesquisa terminar
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//img[@title='Alterar Usuário']")
            )
        )

        alterar = self.driver.find_element(
            By.XPATH,
            "//img[@title='Alterar Usuário']"
        )

        self.driver.execute_script(
            "arguments[0].click();",
            alterar
        )

    # =====================================================
    # ABRIR BOX DO CONTATO
    # =====================================================
    def abrir_alterar_contato(self):

        print("Abrindo modal...")

        self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "imgAlterarContato")
            )
        ).click()

        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[id^='modal-frame']")
            )
        )

        self.wait.until(
            EC.presence_of_element_located(
                (By.ID, "lblFeminino")
            )
        )
    # =====================================================
    # PREENCHER DADOS
    # =====================================================
    def preencher(self, usuario):

        # -------------------------
        # CARGO
        # -------------------------
        cargo_usuario = (usuario.cargo or "").upper()
        sexo = (usuario.sexo or "M").upper()

        if "DELEGAD" in cargo_usuario:
            valor_cargo = "888" if sexo == "F" else "14"
        elif "ESCRIV" in cargo_usuario:
            valor_cargo = "555" if sexo == "F" else "554"
        elif "AGENTE" in cargo_usuario:
            valor_cargo = "546" if sexo == "M" else "545"
        else:
            raise Exception(f"Cargo não reconhecido: {usuario.cargo}")

        print(f"Cargo do usuário: {cargo_usuario}")
        print(f"Sexo: {sexo}")
        print(f"Valor esperado do cargo: {valor_cargo}")

        # -------------------------
        # SEXO
        # -------------------------
        if sexo == "F":
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

        # Aguarda um instante para o sistema atualizar o select
        time.sleep(2)

        # -------------------------
        # SELECT DO CARGO
        # -------------------------
        select = Select(
            self.wait.until(
                EC.presence_of_element_located(
                    (By.ID, "selCargo")
                )
            )
        )

        # Aguarda até que a opção desejada exista
        self.wait.until(
            lambda d: any(
                op.get_attribute("value") == valor_cargo
                for op in Select(
                    d.find_element(By.ID, "selCargo")
                ).options
            )
        )

        Select(
            self.driver.find_element(By.ID, "selCargo")
        ).select_by_value(valor_cargo)

        print(f"[OK] Cargo selecionado (valor={valor_cargo})")

        time.sleep(2)

    # =====================================================
    # SALVAR
    # =====================================================
    def salvar(self):

        # Salva o modal
        self.wait.until(
            EC.element_to_be_clickable(
                (By.NAME, "sbmAlterarContato")
            )
        ).click()

        # Sai do iframe
        self.driver.switch_to.default_content()

        time.sleep(2)

        # Fecha alerta caso exista
        try:
            Alert(self.driver).accept()
            time.sleep(1)
        except:
            pass

        # Salva o usuário
        self.wait.until(
            EC.element_to_be_clickable(
                (By.NAME, "sbmAlterarUsuario")
            )
        ).click()

        time.sleep(3)

        # Fecha alerta caso apareça
        try:
            Alert(self.driver).accept()
            time.sleep(1)
        except:
            pass

        print("[OK] Cadastro no SEI finalizado.")