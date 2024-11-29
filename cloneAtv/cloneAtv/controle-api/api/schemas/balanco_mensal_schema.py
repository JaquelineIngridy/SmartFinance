from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class BalancoMensalSchema(BaseModel):
    id: int
    usuario_id: int
    mes_referencia: date
    receita_total: Decimal
    despesas_totais: Decimal
    saldo_inicial: Decimal
    saldo_final: Decimal

    class Config:
        orm_mode = True