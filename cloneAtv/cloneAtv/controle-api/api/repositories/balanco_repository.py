from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from api.schemas.balanco_mensal_schema import BalancoMensalSchema
from ..models import models

def listar_balancos(db: Session, usuario_id: int, pagina: int = 1, registros: int = 3):
    skip = (pagina - 1) * registros
    balancos = db.scalars(
        select(models.BalancoMensal)
        .where(models.BalancoMensal.usuario_id == usuario_id)
        .order_by(desc(models.BalancoMensal.mes_referencia))
        .offset(skip)
        .limit(registros)
    ).all()
    
    return balancos

def criar_balanco(balanco: BalancoMensalSchema, db: Session):
    db_balanco = models.BalancoMensal(
        usuario_id=balanco.usuario_id,
        mes_referencia=balanco.mes_referencia,
        receita_total=Decimal(balanco.receita_total),
        despesas_totais=Decimal(balanco.despesas_totais),
        saldo_inicial=Decimal(balanco.saldo_inicial),
        saldo_final=Decimal(balanco.saldo_final)
    )

    db.add(db_balanco)
    db.commit()
    db.refresh(db_balanco)

    return BalancoMensalSchema(
        id=db_balanco.id,
        usuario_id=db_balanco.usuario_id,
        mes_referencia=db_balanco.mes_referencia,
        receita_total=db_balanco.receita_total,
        despesas_totais=db_balanco.despesas_totais,
        saldo_inicial=db_balanco.saldo_inicial,
        saldo_final=db_balanco.saldo_final
    )

def atualizar_balanco(id: int, balanco: BalancoMensalSchema, db: Session):
    db_balanco = db.scalar(
        select(models.BalancoMensal).where(models.BalancoMensal.id == id)
    )

    if db_balanco is None:
        raise HTTPException(status_code=404, detail='Balanço não encontrado')

    db_balanco.mes_referencia = balanco.mes_referencia
    db_balanco.receita_total = Decimal(balanco.receita_total)
    db_balanco.despesas_totais = Decimal(balanco.despesas_totais)
    db_balanco.saldo_inicial = Decimal(balanco.saldo_inicial)
    db_balanco.saldo_final = Decimal(balanco.saldo_final)

    db.commit()
    db.refresh(db_balanco)

    return BalancoMensalSchema(
        id=db_balanco.id,
        usuario_id=db_balanco.usuario_id,
        mes_referencia=db_balanco.mes_referencia,
        receita_total=db_balanco.receita_total,
        despesas_totais=db_balanco.despesas_totais,
        saldo_inicial=db_balanco.saldo_inicial,
        saldo_final=db_balanco.saldo_final
    )

def deletar_balanco(id: int, db: Session):
    db_balanco = db.scalar(
        select(models.BalancoMensal).where(models.BalancoMensal.id == id)
    )

    if db_balanco is None:
        raise HTTPException(status_code=404, detail='Balanço não encontrado')

    db.delete(db_balanco)
    db.commit()

    return {"detail": "Balanço removido com sucesso"}