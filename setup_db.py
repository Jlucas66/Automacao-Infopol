import sqlite3
import csv

DB_NAME = 'infopol_teste.db'


def criar_banco_teste():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 🔥 TABELA CORRIGIDA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unidades (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            codigo INTEGER UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT,
            data_nasc TEXT,
            status TEXT DEFAULT 'pendente',
            unidade_id INTEGER,
            FOREIGN KEY (unidade_id) REFERENCES unidades(id)
        )
    ''')

    # 🔥 LIMPA PRA EVITAR DUPLICIDADE
    cursor.execute("DELETE FROM unidades")

    dados = [
        ('Caique Teste 4', '11122233344', '01/01/1990'),
        ('Caique Teste 3', '55566677788', '15/05/1985'),
        ('Caique Teste 4', '99900011122', '20/10/1995'),
        ('Vamberto', '02714983405', '15/09/1988'),
    ]

    cursor.executemany(
        "INSERT INTO pessoas (nome, cpf, data_nasc) VALUES (?, ?, ?)",
        dados
    )

    conn.commit()
    conn.close()
    print("✅ Banco criado com sucesso!")


def importar_unidades_csv(caminho_csv):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    with open(caminho_csv, newline='', encoding='utf-8') as arquivo:
        reader = csv.DictReader(arquivo)

        unidades = []

        for linha in reader:
            nome = linha["NM_UNIDADE_OPERACIONAL"]
            codigo = linha["ID_UNIDADE_OPERACIONAL"]

            if nome and codigo:
                unidades.append((nome.strip(), int(codigo)))

        # 🔥 INSERT CORRETO
        cursor.executemany(
            "INSERT INTO unidades (nome, codigo) VALUES (?, ?)",
            unidades
        )

    conn.commit()
    conn.close()

    print(f"✅ {len(unidades)} unidades importadas!")


if __name__ == "__main__":
    criar_banco_teste()
    importar_unidades_csv("UNIDADE_OPERACIONAL_202604061029.csv")