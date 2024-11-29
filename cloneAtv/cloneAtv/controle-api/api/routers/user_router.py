from fastapi import APIRouter, Depends
from api.schemas.users.user_requisicao_schema import UsuarioInsercaoSchema, UsuarioAtualizacaoSchema
from ..database import Sessionlocal
from sqlalchemy.orm import Session
from ..repositories import user_repository
from ..schemas.users import user_retorno_schema
from api.schemas.users.login_schema import LoginSchema

router = APIRouter()

def get_db():
 
    db_session = Sessionlocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.get("/listar", response_model=list[user_retorno_schema.UsuarioRetornoSchema])
def listar_usuarios(pagina: int = 1, registros: int = 3, tipoRegistros: str = 'A', db: Session = Depends(get_db)):
    return user_repository.listar_usuarios(db, pagina, registros, tipoRegistros)

@router.post("/criar", response_model=user_retorno_schema.UsuarioRetornoSchema)
def criar_usuario(usuario: UsuarioInsercaoSchema, db: Session = Depends(get_db)):
    return user_repository.criar_usuario(usuario, db)

@router.put("/atualizar/{id}", response_model=user_retorno_schema.UsuarioRetornoSchema)
def criar_usuario(id: int, usuario: UsuarioAtualizacaoSchema, db: Session = Depends(get_db)):
    return user_repository.atualizar_usuario(id, usuario, db)


@router.delete("/remover/{id}")
def deletar_usuario(id: int, db: Session = Depends(get_db)):
    return user_repository.deletar_usuario(id, db)

@router.post("/login")
def login(login: LoginSchema, db: Session = Depends(get_db)):
    return user_repository.verificar_login(login.CPF, login.Senha, db)