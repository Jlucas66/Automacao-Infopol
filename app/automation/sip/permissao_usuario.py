import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


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

        Select(
            campo_sistema
        ).select_by_visible_text(
            "SEI"
        )

        self.driver.execute_script(
            "trocarSistema();"
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
        self.wait.until(
            lambda d: any(
                opcao.text.strip() == "Básico"
                for opcao in Select(
                    d.find_element(By.ID, "selPerfil")
                ).options
            )
        )

        Select(
            self.driver.find_element(By.ID, "selPerfil")
        ).select_by_visible_text("Básico")

        # ==========================
        # USUÁRIO
        # ==========================
        campo_usuario = self.driver.find_element(By.ID, "txtUsuario")
        campo_usuario.clear()
        campo_usuario.send_keys(sigla_usuario)

        # Aguarda o item aparecer no dropdown (tag <a> com a sigla)
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//a[contains(text(), '{sigla_usuario}')]")
            )
        )

        # Enter seleciona o primeiro item do dropdown
        campo_usuario.send_keys(Keys.RETURN)
        time.sleep(1)

        # Confirma seleção
        label_nome = self.driver.find_element(By.ID, "lblNomeUsuario")
        print(f"[OK] Usuário selecionado: {label_nome.text.strip()}")

    def salvar(self):
        url_antes = self.driver.current_url

        botao = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "sbmCadastrarPermissao"))
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", botao
        )
        botao.click()  # clique nativo

        # Aguarda confirmação
        try:
            self.wait.until(EC.url_changes(url_antes))
            print("[OK] Permissão salva - página redirecionada.")
        except:
            try:
                mensagem = self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".mensagem-sucesso, .alert-success, #msgSucesso")
                    )
                )

                print(f"[OK] Permissão salva - mensagem: {mensagem.text}")
            except:
                print("[ERRO] Nenhuma confirmação de permissão detectada.")
                print(f"URL atual: {self.driver.current_url}")
                self.driver.save_screenshot("erro_salvar_permissao.png")
                raise Exception("Salvar permissão não confirmado — verifique erro_salvar_permissao.png")