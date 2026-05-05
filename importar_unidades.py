import csv
from db import conectar

def importar_unidades(caminho_csv):
    conn = conectar()
    cursor = conn.cursor()

    with open(caminho_csv, newline='', encoding='utf-8') as arquivo:
        reader = csv.DictReader(arquivo)

        dados = []

        for linha in reader:
            try:
                dados.append((
                    int(linha["ID_UNIDADE_OPERACIONAL"]),
                    linha["NM_UNIDADE_OPERACIONAL"],
                    int(linha["ID_ENTIDADE"]) if linha["ID_ENTIDADE"] else None,
                    linha["DS_COMPLEMENTO"] if linha["DS_COMPLEMENTO"] else None,
                    linha["CD_OPERACIONAL"] if linha["CD_OPERACIONAL"] else None,
                    int(linha["ID_UNIDADE_OPERACIONAL_PAI"]) if linha["ID_UNIDADE_OPERACIONAL_PAI"] else None,
                    linha["FL_CRIACAO_BO"] == "1",
                    linha["FL_CRIACAO_BOF"] == "1",
                    linha["FL_CRIACAO_BOI"] == "1",
                    linha["FL_CRIACAO_IP"] == "1",
                    linha["FL_TREINAMENTO"] == "1",
                    int(linha["ID_PONTO_REFERENCIA"]) if linha["ID_PONTO_REFERENCIA"] else None
                ))
            except Exception as e:
                print(f"⚠️ Erro ao processar linha: {e}")

        cursor.executemany("""
            INSERT INTO unidades (
                id_unidade_operacional,
                nm_unidade_operacional,
                id_entidade,
                ds_complemento,
                cd_operacional,
                id_unidade_operacional_pai,
                fl_criacao_bo,
                fl_criacao_bof,
                fl_criacao_boi,
                fl_criacao_ip,
                fl_treinamento,
                id_ponto_referencia
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_unidade_operacional) DO NOTHING
        """, dados)

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ {len(dados)} unidades importadas com sucesso!")


if __name__ == "__main__":
    importar_unidades("UNIDADE_OPERACIONAL_202604061029.csv")