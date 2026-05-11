import psycopg2


def conectar():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="infopol_db",
        user="postgres",
        password="123456"
    )


def buscar_codigo_unidade(nome):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id_unidade_operacional
        FROM unidades
        WHERE nm_unidade_operacional ILIKE %s
        LIMIT 1
        """,
        (f"%{nome}%",)
    )

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        print(f"🆔 Código encontrado: {resultado[0]}")
        return resultado[0]

    print(f"❌ Unidade '{nome}' não encontrada no banco")
    return None