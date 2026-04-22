import sqlite3
import os

DB_NAME = 'infopol_teste.db'

def conectar_banco():
    """Conecta ao arquivo de banco de dados local (SQLite)."""
    # Isso cria um arquivo chamado 'infopol_teste.db' automaticamente
    return sqlite3.connect(DB_NAME)

def buscar_registros_pendentes():
    """Busca dados no arquivo local."""
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        # Seleciona os dados da tabela que vamos criar logo abaixo
        cursor.execute("SELECT id, nome, cpf, data_nasc FROM pessoas WHERE status = 'pendente' LIMIT 5")
        dados = cursor.fetchall()
        conn.close()
        return dados
    except Exception as e:
        print(f"Aviso: Tabela ainda não existe. Rode o setup primeiro! Erro: {e}")
        return []
    


def buscar_pessoa_por_cpf(cpf):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pessoas WHERE cpf = ?", (cpf,))
    pessoa = cursor.fetchone()

    conn.close()
    return pessoa


def buscar_unidade_por_id(unidade_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM unidades WHERE id = ?", (unidade_id,))
    unidade = cursor.fetchone()

    conn.close()
    return unidade


def atualizar_pessoa(cpf, unidade_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pessoas
        SET unidade_id = ?, status = 'concluido'
        WHERE cpf = ?
    """, (unidade_id, cpf))

    conn.commit()
    conn.close()

    
def atualizar_status_no_banco(id_registro, novo_status):
    """Atualiza o status no arquivo local."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("UPDATE pessoas SET status = ? WHERE id = ?", (novo_status, id_registro))
    conn.commit()
    conn.close()