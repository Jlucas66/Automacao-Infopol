import csv

from app.db.db import conectar


def importar_unidades_csv():
    conn = conectar()
    cursor = conn.cursor()

    caminho_csv = "app/data/UNIDADE_OPERACIONAL_202604061029.csv"

    with open(caminho_csv, newline='', encoding='utf-8') as arquivo:

        reader = csv.DictReader(arquivo)

        total = 0

        for linha in reader:

            try:
                cursor.execute("""
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
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

                    ON CONFLICT (id_unidade_operacional)
                    DO NOTHING
                """, (

                    int(linha["ID_UNIDADE_OPERACIONAL"]),
                    linha["NM_UNIDADE_OPERACIONAL"],

                    int(linha["ID_ENTIDADE"])
                    if linha["ID_ENTIDADE"]
                    else None,

                    linha["DS_COMPLEMENTO"],

                    linha["CD_OPERACIONAL"],

                    int(linha["ID_UNIDADE_OPERACIONAL_PAI"])
                    if linha["ID_UNIDADE_OPERACIONAL_PAI"]
                    else None,

                    linha["FL_CRIACAO_BO"] == "1",
                    linha["FL_CRIACAO_BOF"] == "1",
                    linha["FL_CRIACAO_BOI"] == "1",
                    linha["FL_CRIACAO_IP"] == "1",
                    linha["FL_TREINAMENTO"] == "1",

                    int(linha["ID_PONTO_REFERENCIA"])
                    if linha["ID_PONTO_REFERENCIA"]
                    else None
                ))

                total += 1

            except Exception as e:
                print(f"❌ Erro ao importar linha: {e}")

    conn.commit()

    cursor.close()
    conn.close()

    print(f"✅ {total} unidades importadas!")


if __name__ == "__main__":
    importar_unidades_csv()