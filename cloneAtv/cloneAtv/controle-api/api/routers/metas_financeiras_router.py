from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import Sessionlocal
from ..schemas.metas_financeiras_schema import MetasFinanceiras, MetasFinanceirasCreate
from ..repositories import metas_financeiras_repository as metas_repo

router = APIRouter()

def get_db():
    db_session = Sessionlocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/metas_financeiras/", response_model=MetasFinanceiras)
def create_meta(meta: MetasFinanceirasCreate, db: Session = Depends(get_db)):
    return metas_repo.create_meta(db, meta)

@router.get("/metas_financeiras/{meta_id}", response_model=MetasFinanceiras)
def read_meta(meta_id: int, db: Session = Depends(get_db)):
    db_meta = metas_repo.get_meta(db, meta_id)
    if db_meta is None:
        raise HTTPException(status_code=404, detail="Meta financeira não encontrada")
    return db_meta

@router.put("/metas_financeiras/{meta_id}", response_model=MetasFinanceiras)
def update_meta(meta_id: int, meta: MetasFinanceirasCreate, db: Session = Depends(get_db)):
    db_meta = metas_repo.get_meta(db, meta_id)
    if db_meta is None:
        raise HTTPException(status_code=404, detail="Meta financeira não encontrada")
    return metas_repo.update_meta(db, meta_id, meta)

@router.delete("/metas_financeiras/{meta_id}", response_model=dict)
def delete_meta(meta_id: int, db: Session = Depends(get_db)):
    db_meta = metas_repo.get_meta(db, meta_id)
    if db_meta is None:
        raise HTTPException(status_code=404, detail="Meta financeira não encontrada")
    metas_repo.delete_meta(db, meta_id)
    return {"detail": "Meta financeira excluída com sucesso"}