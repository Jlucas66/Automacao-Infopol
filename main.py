# main.py

from database import (
    buscar_pessoa_por_cpf,
    buscar_unidade_por_id,
    atualizar_pessoa
)

from automation import executar_automacao


# 🧩 Fluxo principal
def processar_cadastro(cpf, unidade_id):
    print("🚀 Iniciando processo...")

    # 1. Buscar pessoa no banco
    pessoa = buscar_pessoa_por_cpf(cpf)

    if not pessoa:
        print("❌ CPF não encontrado no banco.")
        return

    print("✅ Pessoa encontrada!")

    # 2. Buscar unidade
    unidade = buscar_unidade_por_id(unidade_id)

    if not unidade:
        print("❌ Unidade não encontrada.")
        return

    unidade_nome = unidade[1]
    print(f"🏢 Unidade selecionada: {unidade_nome}")

    try:
        # 3. Executar automação
        sucesso = executar_automacao(cpf, unidade_nome)

        # 🔥 4. Só atualiza se deu certo
        if sucesso:
            atualizar_pessoa(cpf, unidade_id)
            print("🎉 Processo finalizado com sucesso!")
        else:
            print("⚠️ Automação falhou. Banco não foi atualizado.")

    except Exception as e:
        print(f"❌ Erro durante o processo: {e}")


# 🚀 Futuro: processamento em lote
def executar_em_lote():
    print("🚀 Modo lote ainda não implementado.")
    print("👉 Aqui você pode buscar registros pendentes no banco.")


# 🔥 Entrada do programa
if __name__ == "__main__":
    print("=== Automação Infopol ===")

    try:
        cpf = input("Digite o CPF: ").strip()
        unidade_id = int(input("Digite o ID da unidade: "))

        processar_cadastro(cpf, unidade_id)

    except ValueError:
        print("❌ ID da unidade deve ser um número.")