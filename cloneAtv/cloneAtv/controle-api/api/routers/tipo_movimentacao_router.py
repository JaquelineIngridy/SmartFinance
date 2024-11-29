from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import Sessionlocal
from ..schemas.tipo_movimentacao_schema import TipoMovimentacao, TipoMovimentacaoCreate
from ..repositories import tipo_movimentacao_repository as tipo_repo

router = APIRouter()

def get_db():
    db_session = Sessionlocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/tipos-movimentacao/", response_model=TipoMovimentacao)
def create_tipo(tipo: TipoMovimentacaoCreate, db: Session = Depends(get_db)):
    return tipo_repo.create_tipo_movimentacao(db, tipo)

@router.get("/tipos-movimentacao/{tipo_id}", response_model=TipoMovimentacao)
def read_tipo(tipo_id: int, db: Session = Depends(get_db)):
    db_tipo = tipo_repo.get_tipo_movimentacao(db, tipo_id)
    if db_tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de movimentação não encontrado")
    return db_tipo

@router.get("/tipos-movimentacao/")
def read_tipos(skip: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    return tipo_repo.get_tipos_movimentacao(db, skip=skip, limit=limit)