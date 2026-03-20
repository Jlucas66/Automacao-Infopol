import sqlite3
import os

def conectar_banco():
    """Conecta ao arquivo de banco de dados local (SQLite)."""
    # Isso cria um arquivo chamado 'dados_teste.db' automaticamente
    return sqlite3.connect('dados_teste.db')

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

def atualizar_status_no_banco(id_registro, novo_status):
    """Atualiza o status no arquivo local."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("UPDATE pessoas SET status = ? WHERE id = ?", (novo_status, id_registro))
    conn.commit()
    conn.close()