from pydantic import BaseModel
from datetime import date

class InvestimentosBase(BaseModel):
    usuario_id: int
    tipo_investimento: str
    valor_investido: float
    data_investido: date
    valor_atual: float

class InvestimentosCreate(InvestimentosBase):
    pass

class Investimentos(InvestimentosBase):
    id: int

    class Config:
        orm_mode = True