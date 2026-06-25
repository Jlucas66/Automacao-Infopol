from dataclasses import dataclass


@dataclass
class Usuario:

    nome: str
    cpf: str
    email: str

    nome_oferta: str | None = None
    dominio: str | None = None

    sexo: str | None = None
    matricula: str | None = None