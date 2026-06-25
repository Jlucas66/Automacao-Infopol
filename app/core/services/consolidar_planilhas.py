from pathlib import Path

import pandas as pd


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
            sheet_name="Matriculados"
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
        # Normaliza CPF
        # ==========================
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

        # ==========================
        # Junta as tabelas
        # ==========================
        df_final = df_acadepol.merge(
            df_completa,
            on="cpf_merge",
            how="left"
        )

        # ==========================
        # Padroniza tudo para minúsculo
        # ==========================
        df_final.columns = (
            df_final.columns
            .str.strip()
            .str.lower()
        )

        return df_final