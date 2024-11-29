from datetime import date
from decimal import Decimal
from pydantic import BaseModel

class MovimentacaoInsercaoSchema(BaseModel):
    UsuarioId: int
    Categoria: str
    Valor: Decimal
    TipoMovimentacaoId: int
    DataMovimentacao: date
    Descricao: str | None

    class Config:
        from_attributes = True
