from db import conectar

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # 🏢 Tabela UNIDADES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unidades (
            id_unidade_operacional INTEGER PRIMARY KEY,
            nm_unidade_operacional TEXT NOT NULL,
            id_entidade INTEGER,
            ds_complemento TEXT,
            cd_operacional TEXT,
            id_unidade_operacional_pai INTEGER,
            fl_criacao_bo BOOLEAN,
            fl_criacao_bof BOOLEAN,
            fl_criacao_boi BOOLEAN,
            fl_criacao_ip BOOLEAN,
            fl_treinamento BOOLEAN,
            id_ponto_referencia INTEGER
        );
    """)

    # 👤 Tabela USUARIOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            cpf VARCHAR(11) UNIQUE NOT NULL,
            matricula TEXT,
            email TEXT,
            data_nascimento DATE,
            unidade_id INTEGER,
            FOREIGN KEY (unidade_id)
                REFERENCES unidades(id_unidade_operacional)
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Tabelas verificadas/criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()