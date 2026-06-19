from app.automation.sip.login import LoginSip
from app.automation.sip.cadastro_usuario import CadastroUsuario


class SipAutomation:

    def __init__(self, driver):

        self.driver = driver

        self.login = LoginSip(driver)
        self.cadastro = CadastroUsuario(driver)

    def executar(self, usuarios):

        self.login.realizar_login(
            usuario="admin",
            senha="123"
        )

        for usuario in usuarios:

            self.cadastro.cadastrar(
                usuario
            )