from pathlib import Path

import pandas as pd

from app.core.models.usuario import Usuario


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

        df = pd.read_excel(
            caminho,
            sheet_name="Matriculados"
        )

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
                email=str(linha["email "]).strip(),

                nome_oferta=str(
                    linha["nome_oferta"]
                ).strip(),

                dominio=(
                    str(linha["DOMINIO "]).strip()
                    if pd.notna(linha["DOMINIO "])
                    else None
                )
            )

            usuarios.append(usuario)

        return usuarios