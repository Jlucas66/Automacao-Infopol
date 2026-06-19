from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginSip:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def realizar_login(self, usuario, senha):

        self.wait.until(
            EC.presence_of_element_located(
                (By.ID, "txtUsuario")
            )
        ).send_keys(usuario)

        self.driver.find_element(
            By.ID,
            "pwdSenha"
        ).send_keys(senha)

        Select(
            self.driver.find_element(
                By.ID,
                "selOrgao"
            )
        ).select_by_visible_text(
            "PCPE"
        )

        self.driver.find_element(
            By.ID,
            "sbmAcessar"
        ).click()