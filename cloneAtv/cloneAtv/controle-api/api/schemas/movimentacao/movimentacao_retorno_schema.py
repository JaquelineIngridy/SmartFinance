from datetime import date, datetime
import decimal
from pydantic import BaseModel



class UsuarioMovimentacao(BaseModel):
    Id: int
    CPF: str
    Nome: str
    Email: str

    
    class Config():
        orm_mode = True

class TipoMovimentacao(BaseModel):
    Id: int
    Codigo: str
    Descricao: str

    
    class Config():
        orm_mode = True


class MovimentacaoRetornoSchema(BaseModel):
    Id: int
    UsuarioMovimentacao: UsuarioMovimentacao
    Categoria: str
    Valor: decimal.Decimal
    TipoMovimentacao: TipoMovimentacao
    DataMovimentacao: date
    Descricao: str
    DataCriacao: datetime
    DataPrevista: date | None
    DataFim: datetime | None
    DataAtualizacao: datetime | None

    class Config():
        from_attributes = True
        arbitrary_types_allowed=True