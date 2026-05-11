import sqlite3

conn = sqlite3.connect('infopol_teste.db')
cursor = conn.cursor()

cursor.execute("SELECT id, nome, codigo FROM unidades")

dados = cursor.fetchall()

for d in dados:
    print(d)

conn.close()