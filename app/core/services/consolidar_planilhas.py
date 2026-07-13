# from pathlib import Path

# import pandas as pd


# class ConsolidadorPlanilhas:

#     @staticmethod
#     def consolidar(
#         caminho_acadepol: str,
#         caminho_completa: str
#     ) -> pd.DataFrame:

#         if not Path(caminho_acadepol).exists():
#             raise FileNotFoundError(caminho_acadepol)

#         if not Path(caminho_completa).exists():
#             raise FileNotFoundError(caminho_completa)

#         # ==========================
#         # Lê as planilhas
#         # ==========================
#         df_acadepol = pd.read_excel(
#             caminho_acadepol,
#             sheet_name="Matriculados"
#         )

#         df_completa = pd.read_excel(
#             caminho_completa
#         )

#         # ==========================
#         # Limpa nomes das colunas
#         # ==========================
#         df_acadepol.columns = (
#             df_acadepol.columns
#             .str.strip()
#             .str.replace("\n", " ", regex=False)
#         )

#         df_completa.columns = (
#             df_completa.columns
#             .str.strip()
#             .str.replace("\n", " ", regex=False)
#         )

#         # ==========================
#         # Renomeia colunas da tabela completa
#         # ==========================
#         df_completa = df_completa.rename(
#             columns={
#                 "CPF": "cpf",
#                 "SEXO": "sexo",
#                 "MATRICULA_NOVA*": "matricula_nova",
#                 "DATA_DE_ADMISSAO*": "data_admissao",
#                 "PAI": "pai",
#                 "MAE": "mae",
#             }
#         )

#         # ==========================
#         # Normaliza CPF
#         # ==========================
#         df_acadepol["cpf_merge"] = (
#             pd.to_numeric(
#                 df_acadepol["cpf corrigido"],
#                 errors="coerce"
#             )
#             .fillna(0)
#             .astype("int64")
#             .astype(str)
#         )

#         df_completa["cpf_merge"] = (
#             pd.to_numeric(
#                 df_completa["cpf"],
#                 errors="coerce"
#             )
#             .fillna(0)
#             .astype("int64")
#             .astype(str)
#         )

#         # ==========================
#         # Junta as tabelas
#         # ==========================
#         df_final = df_acadepol.merge(
#             df_completa,
#             on="cpf_merge",
#             how="left"
#         )

#         # ==========================
#         # Padroniza tudo para minúsculo
#         # ==========================
#         df_final.columns = (
#             df_final.columns
#             .str.strip()
#             .str.lower()
#         )

#         return df_final

from pathlib import Path
import unicodedata

import pandas as pd


def normalizar_nome(nome):

    if pd.isna(nome):
        return ""

    nome = str(nome).upper().strip()

    nome = unicodedata.normalize("NFKD", nome)

    nome = "".join(
        c for c in nome
        if not unicodedata.combining(c)
    )

    return " ".join(nome.split())


class ConsolidadorPlanilhas:

    @staticmethod
    def consolidar(
        caminho_acadepol: str,
        caminho_completa: str
    ) -> pd.DataFrame:

        if not Path(caminho_acadepol).exists():
            raise FileNotFoundError(caminho_acadepol)

        if not Path(caminho_completa).exists():
            raise FileNotFoundError(caminho_completa)

        # ==========================
        # Lê as planilhas
        # ==========================
        df_acadepol = pd.read_excel(
            caminho_acadepol,
            sheet_name=0
        )

        df_completa = pd.read_excel(
            caminho_completa
        )

        # ==========================
        # Limpa nomes das colunas
        # ==========================
        df_acadepol.columns = (
            df_acadepol.columns
            .str.strip()
            .str.replace("\n", " ", regex=False)
        )

        df_completa.columns = (
            df_completa.columns
            .str.strip()
            .str.replace("\n", " ", regex=False)
        )

        # ==========================
        # Padroniza nomes das colunas da ACADEPOL
        # ==========================
        df_acadepol = df_acadepol.rename(
            columns={
                "E-MAIL": "email",
                "DOMINIO": "dominio"
            }
        )

        # ==========================
        # Renomeia colunas da tabela completa
        # ==========================
        df_completa = df_completa.rename(
            columns={
                "CPF": "cpf",
                "SEXO": "sexo",
                "MATRICULA_NOVA*": "matricula_nova",
                "DATA_DE_ADMISSAO*": "data_admissao",
                "PAI": "pai",
                "MAE": "mae",
            }
        )

        # ==========================
        # Junta as tabelas
        # ==========================
        if "cpf corrigido" in df_acadepol.columns:

            print(">> Fazendo merge pelo CPF")

            df_acadepol["cpf_merge"] = (
                pd.to_numeric(
                    df_acadepol["cpf corrigido"],
                    errors="coerce"
                )
                .fillna(0)
                .astype("int64")
                .astype(str)
            )

            df_completa["cpf_merge"] = (
                pd.to_numeric(
                    df_completa["cpf"],
                    errors="coerce"
                )
                .fillna(0)
                .astype("int64")
                .astype(str)
            )

            df_final = df_acadepol.merge(
                df_completa,
                on="cpf_merge",
                how="left"
            )

        else:

            print(">> Fazendo merge pelo NOME")

            df_acadepol["nome_merge"] = (
                df_acadepol["nome_pessoa"]
                .apply(normalizar_nome)
            )

            df_completa["nome_merge"] = (
                df_completa["NOME"]
                .apply(normalizar_nome)
            )

            df_final = df_acadepol.merge(
                df_completa,
                on="nome_merge",
                how="left"
            )

        print("\nCOLUNAS DO DF_FINAL:")
        print(df_final.columns.tolist())

        print("\n===== RESULTADO DO MERGE =====")

        colunas_debug = [
            c for c in [
                "nome_pessoa",
                "cpf",
                "email",
                "sexo",
                "matricula_nova"
            ]
            if c in df_final.columns
        ]

        print(df_final[colunas_debug].head(10))

        # ==========================
        # Padroniza tudo para minúsculo
        # ==========================
        df_final.columns = (
            df_final.columns
            .str.strip()
            .str.lower()
        )

        return df_final