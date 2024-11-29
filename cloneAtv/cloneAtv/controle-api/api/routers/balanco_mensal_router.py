from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.balanco_mensal_schema import BalancoMensalSchema
from ..database import Sessionlocal
from ..repositories import balanco_repository

router = APIRouter()

def get_db():
    db_session = Sessionlocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.get("/listar", response_model=list[BalancoMensalSchema])
def listar_balancos(usuario_id: int, pagina: int = 1, registros: int = 3, db: Session = Depends(get_db)):
    return balanco_repository.listar_balancos(db, usuario_id, pagina, registros)

@router.post("/criar", response_model=BalancoMensalSchema)
def criar_balanco(balanco: BalancoMensalSchema, db: Session = Depends(get_db)):
    return balanco_repository.criar_balanco(balanco, db)

@router.put("/atualizar/{id}", response_model=BalancoMensalSchema)
def atualizar_balanco(id: int, balanco: BalancoMensalSchema, db: Session = Depends(get_db)):
    return balanco_repository.atualizar_balanco(id, balanco, db)

@router.delete("/remover/{id}")
def deletar_balanco(id: int, db: Session = Depends(get_db)):
    return balanco_repository.deletar_balanco(id, db)