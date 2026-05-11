from app.db.db import conectar

def inserir_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    usuarios = [
        ("Caique Teste", "11122233344", "MAT001", "caique@email.com", "1990-01-01", 1999),
        ("Outro Usuario", "55566677788", "MAT002", "outro@email.com", "1985-05-15", 1999),
        ("Vamberto", "02714983405", "MAT003", "teste@teste.com", "1985-05-15", 1999)
    ]

    cursor.executemany("""
        INSERT INTO usuarios (
            nome, cpf, matricula, email, data_nascimento, unidade_id
        ) VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (cpf) DO NOTHING
    """, usuarios)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Usuários inseridos com sucesso!")


if __name__ == "__main__":
    inserir_usuarios()