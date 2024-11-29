from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import Sessionlocal
from ..repositories import movimentacao_repository
from ..schemas.movimentacao import movimentacao_retorno_schema
from api.schemas.movimentacao.movimentacao_retorno_schema import MovimentacaoRetornoSchema
from api.schemas.movimentacao.movimentacao_requisicao_schema import MovimentacaoInsercaoSchema

router = APIRouter()

def get_db():
    db_session = Sessionlocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/movimentacao/criar", response_model=MovimentacaoInsercaoSchema)
def criar_movimentacao(movimentacao: MovimentacaoInsercaoSchema, db: Session = Depends(get_db)):
    return movimentacao_repository.criar_movimentacao(movimentacao, db)

@router.get("/listar/{id}", response_model=list[movimentacao_retorno_schema.MovimentacaoRetornoSchema])
def listar_movimentacoes_usuario(id: int, db: Session = Depends(get_db)):
    return movimentacao_repository.listar_movimentacao_usuario(id, db)