from pydantic import BaseModel

class TipoMovimentacaoBase(BaseModel):
    Codigo: str
    Descricao: str
    Id: int

class TipoMovimentacaoCreate(TipoMovimentacaoBase):
    pass

class TipoMovimentacao(TipoMovimentacaoBase):
    Id: int

    class Config:
        orm_mode = True