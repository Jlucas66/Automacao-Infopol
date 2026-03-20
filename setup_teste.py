import sqlite3

conn = sqlite3.connect('dados_teste.db')
cursor = conn.cursor()

# Criando a tabela de teste
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cpf TEXT,
        data_nasc TEXT,
        status TEXT DEFAULT 'pendente'
    )
''')

# Inserindo 3 nomes para o robô ter o que fazer
testes = [
    ('Caique Nunes Teste 3', '11122233343', '01/01/2001'),
    ('Fulano da Silva 2', '55566677787', '15/05/1991'),
    ('Polícia Civil Teste 2', '00000000001', '21/04/1800')
]

cursor.executemany("INSERT INTO pessoas (nome, cpf, data_nasc) VALUES (?, ?, ?)", testes)
conn.commit()
conn.close()
print("✅ Banco de teste criado com 3 registros pendentes!")