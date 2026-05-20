from app.db.db import conectar


# =========================
# USUÁRIOS
# =========================

def buscar_pessoa_por_cpf(cpf):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM usuarios
        WHERE cpf = %s
        """,
        (cpf,)
    )

    pessoa = cursor.fetchone()

    cursor.close()
    conn.close()

    return pessoa


def atualizar_pessoa(cpf, unidade_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE usuarios
        SET id_unidade_operacional = %s
        WHERE cpf = %s
        """,
        (unidade_id, cpf)
    )

    conn.commit()

    cursor.close()
    conn.close()

    print("✅ Usuário atualizado no PostgreSQL!")


# =========================
# UNIDADES
# =========================

def buscar_unidade_por_id(unidade_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id_unidade_operacional,
            nm_unidade_operacional
        FROM unidades
        WHERE id_unidade_operacional = %s
        """,
        (unidade_id,)
    )

    unidade = cursor.fetchone()

    cursor.close()
    conn.close()

    return unidade


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

def listar_unidades():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id_unidade_operacional,
            nm_unidade_operacional
        FROM unidades
        ORDER BY nm_unidade_operacional
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados