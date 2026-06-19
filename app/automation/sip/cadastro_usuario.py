from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.automation.sip.utils import gerar_sigla


class CadastroUsuario:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def abrir_tela_novo_usuario(self):

        self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "linkMenu11")
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "linkMenu12")
            )
        ).click()

    def preencher(self, usuario):

        # órgão
        Select(
            self.wait.until(
                EC.presence_of_element_located(
                    (By.ID, "selOrgao")
                )
            )
        ).select_by_visible_text("PCPE")

        sigla = gerar_sigla(usuario.email)

        # sigla
        campo_sigla = self.driver.find_element(
            By.ID,
            "txtSigla"
        )
        campo_sigla.clear()
        campo_sigla.send_keys(sigla)

        # nome
        campo_nome = self.driver.find_element(
            By.ID,
            "txtNome"
        )
        campo_nome.clear()
        campo_nome.send_keys(usuario.nome)

        # nome social
        campo_nome_social = self.driver.find_element(
            By.ID,
            "txtNomeSocial"
        )
        campo_nome_social.clear()
        campo_nome_social.send_keys(usuario.nome)

        # CPF
        campo_cpf = self.driver.find_element(
            By.ID,
            "txtCpf"
        )
        campo_cpf.clear()
        campo_cpf.send_keys(usuario.cpf)

        # email
        campo_email = self.driver.find_element(
            By.ID,
            "txtEmail"
        )
        campo_email.clear()
        campo_email.send_keys(usuario.email)

    def salvar(self):

        self.driver.find_element(
            By.NAME,
            "sbmCadastrarUsuario"
        ).click()