from sqlalchemy.orm import Session
from ..models import models
from ..schemas.investimentos_schema import InvestimentosCreate

def create_investimento(db: Session, investimento: InvestimentosCreate):
    db_investimento = models.Investimentos(**investimento.dict())
    db.add(db_investimento)
    db.commit()
    db.refresh(db_investimento)
    return db_investimento

def get_investimento(db: Session, investimento_id: int):
    return db.query(models.Investimentos).filter(models.Investimentos.id == investimento_id).first()

def update_investimento(db: Session, investimento_id: int, investimento: InvestimentosCreate):
    db_investimento = get_investimento(db, investimento_id)
    if db_investimento:
        for key, value in investimento.dict().items():
            setattr(db_investimento, key, value)
        db.commit()
        db.refresh(db_investimento)
    return db_investimento

def delete_investimento(db: Session, investimento_id: int):
    db_investimento = get_investimento(db, investimento_id)
    if db_investimento:
        db.delete(db_investimento)
        db.commit()