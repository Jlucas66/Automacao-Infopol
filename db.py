import sqlite3

DB_NAME = "infopol_teste.db"

def buscar_codigo_unidade(nome):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT codigo FROM unidades WHERE LOWER(nome) LIKE LOWER(?)",
        (f"%{nome}%",)
    )

    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        print(f"🆔 Código encontrado: {resultado[0]}")
        return resultado[0]

    print("❌ Unidade não encontrada no banco")
    return None