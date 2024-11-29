from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import Sessionlocal
from ..schemas.investimentos_schema import Investimentos, InvestimentosCreate
from ..repositories import investimentos_repository as investimentos_repo

router = APIRouter()

def get_db():
    db_session = Sessionlocal()
    try:
        yield db_session
    finally:
        db_session.close()


@router.post("/investimentos/", response_model=Investimentos)
def create_investimento(investimento: InvestimentosCreate, db: Session = Depends(get_db)):
    return investimentos_repo.create_investimento(db, investimento)

@router.get("/investimentos/{investimento_id}", response_model=Investimentos)
def read_investimento(investimento_id: int, db: Session = Depends(get_db)):
    db_investimento = investimentos_repo.get_investimento(db, investimento_id)
    if db_investimento is None:
        raise HTTPException(status_code=404, detail="Investimento não encontrado")
    return db_investimento

@router.put("/investimentos/{investimento_id}", response_model=Investimentos)
def update_investimento(investimento_id: int, investimento: InvestimentosCreate, db: Session = Depends(get_db)):
    db_investimento = investimentos_repo.get_investimento(db, investimento_id)
    if db_investimento is None:
        raise HTTPException(status_code=404, detail="Investimento não encontrado")
    return investimentos_repo.update_investimento(db, investimento_id, investimento)

@router.delete("/investimentos/{investimento_id}", response_model=dict)
def delete_investimento(investimento_id: int, db: Session = Depends(get_db)):
    db_investimento = investimentos_repo.get_investimento(db, investimento_id)
    if db_investimento is None:
        raise HTTPException(status_code=404, detail="Investimento não encontrado")
    investimentos_repo.delete_investimento(db, investimento_id)
    return {"detail": "Investimento excluído com sucesso"}