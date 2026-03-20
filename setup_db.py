import sqlite3

def criar_banco_teste():
    # Cria o arquivo do banco na pasta atual
    conn = sqlite3.connect('infopol_teste.db')
    cursor = conn.cursor()

    # Cria a tabela
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT,
            data_nasc TEXT,
            status TEXT DEFAULT 'pendente'
        )
    ''')

    # Insere dados de teste
    dados = [
        ('Caique Teste 4', '11122233344', '01/01/1990'),
        ('Caique Teste 3', '55566677788', '15/05/1985'),
        ('Caique Teste 4', '99900011122', '20/10/1995')
    ]

    cursor.executemany("INSERT INTO pessoas (nome, cpf, data_nasc) VALUES (?, ?, ?)", dados)
    
    conn.commit()
    conn.close()
    print("✅ Banco de dados SQLite criado com sucesso!")

if __name__ == "__main__":
    criar_banco_teste()