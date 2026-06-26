from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clicar(driver, xpath, timeout=20):

    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath)
        )
    ).click()


def preencher(driver, xpath, texto, timeout=20):

    campo = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)
        )
    )

    campo.clear()
    campo.send_keys(texto)

def gerar_sigla(email: str) -> str:
    """
    joao.lucas@policiacivil.pe.gov.br
    -> joao.lucas
    """

    return email.split("@")[0].strip().lower()    