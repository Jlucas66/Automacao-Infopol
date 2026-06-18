from dataclasses import dataclass


@dataclass
class Usuario:
    nome: str
    cpf: str
    email: str

    nome_oferta: str | None = None
    dominio: str | None = None