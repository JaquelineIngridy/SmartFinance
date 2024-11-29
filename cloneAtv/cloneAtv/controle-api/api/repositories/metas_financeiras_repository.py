from sqlalchemy.orm import Session
from ..models import models
from ..schemas.metas_financeiras_schema import MetasFinanceirasCreate

def create_meta(db: Session, meta: MetasFinanceirasCreate):
    db_meta = models.MetasFinanceiras(**meta.dict())
    db.add(db_meta)
    db.commit()
    db.refresh(db_meta)
    return db_meta

def get_meta(db: Session, meta_id: int):
    return db.query(models.MetasFinanceiras).filter(models.MetasFinanceiras.id == meta_id).first()

def update_meta(db: Session, meta_id: int, meta: MetasFinanceirasCreate):
    db_meta = get_meta(db, meta_id)
    if db_meta:
        for key, value in meta.dict().items():
            setattr(db_meta, key, value)
        db.commit()
        db.refresh(db_meta)
    return db_meta

def delete_meta(db: Session, meta_id: int):
    db_meta = get_meta(db, meta_id)
    if db_meta:
        db.delete(db_meta)
        db.commit()