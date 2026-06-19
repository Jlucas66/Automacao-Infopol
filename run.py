# run.py

from app.core.main import processar_cadastro
from app.core.services.leitor_planilha import LeitorPlanilha
from app.automation.sip.sip_automation import SipAutomation

if __name__ == "__main__":
    print("=== Automação Infopol ===")

    cpf = input("Digite o CPF: ").strip()
    unidade_id = int(input("Digite o ID da unidade: "))

    processar_cadastro(cpf, unidade_id)