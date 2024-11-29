from pydantic import BaseModel
from datetime import date

class OrcamentoMensalBase(BaseModel):
    mes_referencia: date
    valor_orcamento: float
    valor_gasto: float

class OrcamentoMensalCreate(OrcamentoMensalBase):
    pass

class OrcamentoMensal(OrcamentoMensalBase):
    id: int
    usuario_id: int

    class Config:
        orm_mode = True