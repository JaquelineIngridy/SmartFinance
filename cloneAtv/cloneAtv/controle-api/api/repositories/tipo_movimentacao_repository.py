from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from ..models import models
from ..schemas.tipo_movimentacao_schema import TipoMovimentacaoCreate

def get_tipo_movimentacao(db: Session, tipo_id: int):
    return db.query(models.TipoMovimentacao).filter(models.TipoMovimentacao.Id == tipo_id).first()

def get_tipos_movimentacao(db: Session, skip: int = 0, limit: int = 10):
    skip = (skip - 1) * limit
    resultado=db.scalars(
                select(models.TipoMovimentacao).order_by(desc(models.TipoMovimentacao.Id)).offset(skip).limit(limit)
        ).all()


    return resultado

def create_tipo_movimentacao(db: Session, tipo: TipoMovimentacaoCreate):
    db_tipo = models.TipoMovimentacao(codigo=tipo.codigo, descricao=tipo.descricao)
    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)
    return db_tipo