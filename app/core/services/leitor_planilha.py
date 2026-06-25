from pathlib import Path

import pandas as pd

from app.core.models.usuario import Usuario
from app.core.services.consolidar_planilhas import ConsolidadorPlanilhas


class LeitorPlanilha:

    @staticmethod
    def carregar(
        caminho: str,
        cargo: str | None = None
    ) -> list[Usuario]:

        arquivo = Path(caminho)

        if not arquivo.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {caminho}"
            )

        # df = pd.read_excel(
        #     caminho,
        #     sheet_name="Matriculados"
        # )
        df = ConsolidadorPlanilhas.consolidar(
            caminho_acadepol=caminho,
            caminho_completa="app/data/tabela-completa.xlsx"
        )
        print(df.columns.tolist())

        # Filtra o cargo se informado
        if cargo:
            df = df[
                df["nome_oferta"].str.contains(
                    cargo,
                    case=False,
                    na=False
                )
            ]

        usuarios = []

        for _, linha in df.iterrows():

            usuario = Usuario(
                nome=str(linha["nome_pessoa"]).strip(),
                cpf = (
                    str(int(linha["cpf corrigido"]))
                    if pd.notna(linha["cpf corrigido"])
                    else ""
                ),
                email=str(linha["email"]).strip(),

                nome_oferta=str(
                    linha["nome_oferta"]
                ).strip(),

                dominio=(
                    str(linha["dominio"]).strip()
                    if pd.notna(linha["dominio"])
                    else None
                ),

                sexo=(
                    str(linha["sexo"]).strip()
                    if pd.notna(linha["sexo"])
                    else None
                ),

                matricula=(
                    str(linha["matricula_nova"]).strip()
                    if pd.notna(linha["matricula_nova"])
                    else None
                )
            )
            print(usuario)

            usuarios.append(usuario)

        return usuarios