import psycopg2


def conectar():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="infopol_db",
        user="postgres",
        password="123456"
    )