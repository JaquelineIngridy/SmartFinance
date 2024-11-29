import base64
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class UsuarioRetornoSchema(BaseModel):
    Id: int
    CPF: str
    Nome: str
    Email: str
    DataNascimento: date
    DataCriacao: datetime
    DataAtualizacao: datetime | None
    DataFim: datetime | None
    Sexo: str
    Senha: Optional[str] | None

    class Config:
        orm_mode = True