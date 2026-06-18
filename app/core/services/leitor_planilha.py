from pathlib import Path

import pandas as pd

from app.core.models.usuario import Usuario


class LeitorPlanilha:

    @staticmethod
    def carregar(caminho: str) -> list[Usuario]:
        print(f"Lendo arquivo: {caminho}")

        arquivo = Path(caminho)

        if not arquivo.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {caminho}"
            )

        df = pd.read_excel(caminho, sheet_name="Matriculados")
        df.columns = df.columns.str.strip()  # Remover espaços em branco dos nomes das colunas
        print("Primeiras ofertas encontradas")
        print(df["nome_oferta"].head(20))  # Verificar as primeiras linhas do DataFrame

        usuarios = []

        for _, linha in df.iterrows():

            usuario = Usuario(
                nome=str(linha["nome_pessoa"]).strip(),
                cpf=str(linha["cpf corrigido"]).strip(),
                email=str(linha["email"]).strip(),

                nome_oferta=(
                    str(linha["nome_oferta"]).strip()
                    if pd.notna(linha["nome_oferta"])
                    else None
                ),

                dominio=(
                    str(linha["DOMINIO"]).strip()
                    if "DOMINIO" in df.columns
                    and pd.notna(linha["DOMINIO"])
                    else None
                )
            )

            usuarios.append(usuario)

        return usuarios