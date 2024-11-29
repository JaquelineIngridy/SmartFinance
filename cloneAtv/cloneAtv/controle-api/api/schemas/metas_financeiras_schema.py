from pydantic import BaseModel
from datetime import date

class MetasFinanceirasBase(BaseModel):
    usuario_id: int
    descricao_meta: str
    valor_meta: float
    valor_atual: float
    data_limite: date

class MetasFinanceirasCreate(MetasFinanceirasBase):
    pass

class MetasFinanceiras(MetasFinanceirasBase):
    id: int

    class Config:
        orm_mode = True