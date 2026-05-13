from fastapi import FastAPI

from app.db.database import (
    buscar_pessoa_por_cpf,
    buscar_unidade_por_id
)

from app.automation.automation import executar_automacao

app = FastAPI()


# =========================
# TESTE
# =========================

@app.get("/")
def home():
    return {"status": "API ONLINE"}


# =========================
# BUSCAR USUÁRIO
# =========================

@app.get("/usuarios/{cpf}")
def buscar_usuario(cpf: str):

    pessoa = buscar_pessoa_por_cpf(cpf)

    if not pessoa:
        return {"erro": "Usuário não encontrado"}

    return {
        "dados": pessoa
    }


# =========================
# BUSCAR UNIDADE
# =========================

@app.get("/unidades/{id_unidade}")
def buscar_unidade(id_unidade: int):

    unidade = buscar_unidade_por_id(id_unidade)

    if not unidade:
        return {"erro": "Unidade não encontrada"}

    return {
        "dados": unidade
    }


# =========================
# EXECUTAR AUTOMAÇÃO
# =========================

@app.post("/executar")
def executar(cpf: str, unidade_id: int):

    unidade = buscar_unidade_por_id(unidade_id)

    if not unidade:
        return {"erro": "Unidade não encontrada"}

    unidade_nome = unidade[1]

    sucesso = executar_automacao(cpf, unidade_nome)

    return {
        "sucesso": sucesso
    }