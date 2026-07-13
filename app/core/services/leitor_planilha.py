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

        df = ConsolidadorPlanilhas.consolidar(
            caminho_acadepol=caminho,
            caminho_completa="app/data/tabela-completa.xlsx"
        )

        # Padroniza os nomes das colunas
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
        )

        # Algumas planilhas usam "cargo"
        if "cargo" in df.columns and "nome_oferta" not in df.columns:
            df = df.rename(columns={"cargo": "nome_oferta"})

        # Algumas planilhas usam "e-mail"
        if "e-mail" in df.columns and "email" not in df.columns:
            df = df.rename(columns={"e-mail": "email"})

        # Algumas planilhas usam "domínio"
        if "domínio" in df.columns and "dominio" not in df.columns:
            df = df.rename(columns={"domínio": "dominio"})

        # Filtra o cargo solicitado
        if cargo:
            df = df[
                df["nome_oferta"].astype(str).str.contains(
                    cargo,
                    case=False,
                    na=False
                )
            ]

        usuarios = []

        for _, linha in df.iterrows():

            cpf = ""

            if "cpf" in df.columns and pd.notna(linha["cpf"]):
                try:
                    cpf = str(int(float(linha["cpf"])))
                except Exception:
                    cpf = str(linha["cpf"]).strip()

            usuario = Usuario(
                nome=str(linha.get("nome_pessoa", "")).strip(),

                cpf=cpf,

                email=str(
                    linha.get("email", "")
                ).strip(),

                nome_oferta=(
                    str(linha.get("nome_oferta", "")).strip()
                    if pd.notna(linha.get("nome_oferta"))
                    else None
                ),

                dominio=(
                    str(linha.get("dominio", "")).strip()
                    if pd.notna(linha.get("dominio"))
                    else None
                ),

                sexo=(
                    str(linha.get("sexo", "")).strip()
                    if pd.notna(linha.get("sexo"))
                    else None
                ),

                matricula=(
                    str(linha.get("matricula_nova", "")).strip()
                    if pd.notna(linha.get("matricula_nova"))
                    else None
                ),

                cargo=(
                    str(linha.get("nome_oferta", "")).strip()
                    if pd.notna(linha.get("nome_oferta"))
                    else None
                )
            )

            usuarios.append(usuario)

        return usuarios