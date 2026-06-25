import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PermissaoUsuario:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def abrir_permissoes(self):

        self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "linkMenu2")
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "linkMenu5")
            )
        ).click()

    def abrir_nova_permissao(self):

        self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "btnNova")
            )
        ).click()

    def preencher(
        self,
        sigla_usuario
    ):

        # ==========================
        # SISTEMA
        # ==========================
        campo_sistema = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "selSistema")
            )
        )

        self.wait.until(
            lambda d: any(
                opcao.text.strip() == "SEI"
                for opcao in Select(
                    d.find_element(By.ID, "selSistema")
                ).options
            )
        )

        Select(campo_sistema).select_by_visible_text(
            "SEI"
        )

        time.sleep(2)

        # ==========================
        # ÓRGÃO UNIDADE
        # ==========================
        Select(
            self.wait.until(
                EC.presence_of_element_located(
                    (By.ID, "selOrgaoUnidade")
                )
            )
        ).select_by_visible_text(
            "PCPE"
        )

        time.sleep(5)

        # ==========================
        # UNIDADE
        # ==========================
        self.wait.until(
            lambda d: any(
                "PCPE - DTI - ASSESSORIA" in opcao.text
                for opcao in Select(
                    d.find_element(
                        By.ID,
                        "selUnidade"
                    )
                ).options
            )
        )

        Select(
            self.driver.find_element(
                By.ID,
                "selUnidade"
            )
        ).select_by_visible_text(
            "PCPE - DTI - ASSESSORIA"
        )

        # ==========================
        # ÓRGÃO USUÁRIO
        # ==========================
        Select(
            self.driver.find_element(
                By.ID,
                "selOrgaoUsuario"
            )
        ).select_by_visible_text(
            "PCPE"
        )

        # ==========================
        # PERFIL
        # ==========================

        select_perfil = Select(
            self.driver.find_element(
              By.ID,
             "selPerfil"
            )
        )

        for opcao in select_perfil.options:

            texto = opcao.text.strip()

            if texto == "Básico":

               opcao.click()
               break

        # ==========================
        # USUÁRIO
        # ==========================
        campo_usuario = self.driver.find_element(
            By.ID,
            "txtUsuario"
        )

        campo_usuario.clear()

        campo_usuario.send_keys(
            sigla_usuario
        )

    def salvar(self):

        self.wait.until(
            EC.element_to_be_clickable(
                (By.NAME, "sbmCadastrarPermissao")
            )
        ).click()