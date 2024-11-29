import base64
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import Sequence, desc, null, select
from sqlalchemy.orm import Session
from api.schemas.users.user_requisicao_schema import UsuarioInsercaoSchema, UsuarioAtualizacaoSchema
from ..models import models
from ..schemas.users import user_retorno_schema
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext

# Contexto para hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para verificar as credenciais e gerar token
def verificar_login(cpf: str, senha: str, db: Session):
    usuario = db.scalar(select(models.Usuario).where(models.Usuario.CPF == cpf))

    if usuario is None or not pwd_context.verify(senha, usuario.Senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Gerar o token JWT
    token_expires = timedelta(hours=1)
    token = jwt.encode({
        "sub": usuario.CPF,
        "exp": datetime.utcnow() + token_expires
    }, "seu_segredo_7004f925da395ba9af4ba7acf1ab2ba73dea83a7fe72798e14bdca97d67d10bbaqui", algorithm="HS256")

    return {"access_token": token, "token_type": "bearer"}

def criar_usuario(usuario: UsuarioInsercaoSchema, db: Session):
    senha_hash = pwd_context.hash(usuario.Senha)

    db_usuario = models.Usuario(
        Nome=usuario.Nome,
        CPF=usuario.CPF,
        Email=usuario.Email,
        DataNascimento=usuario.DataNascimento,
        DataCriacao=usuario.DataCriacao,
        Sexo=usuario.Sexo,
        Senha=senha_hash
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    
def listar_usuarios(db: Session, pagina: int = 1, registros: int = 3, filtro: str = 'A'):
    skip = (pagina - 1) * registros
    usuarios = Sequence[models.Usuario]

    if filtro.upper() == 'A':
        usuarios = db.scalars(
                select(models.Usuario).where(models.Usuario.DataFim == None).order_by(desc(models.Usuario.Id)).offset(skip).limit(registros)
        ).all()
        
    if filtro.upper() == 'I':
            usuarios = db.scalars(
            select(models.Usuario).where(models.Usuario.DataFim != None).order_by(desc(models.Usuario.Id)).offset(skip).limit(registros)
        ).all()

    if filtro.upper() != 'A' and filtro.upper() != 'I':
        usuarios = db.scalars(
                select(models.Usuario).order_by(desc(models.Usuario.Id)).offset(skip).limit(registros)
            ).all()

    for usuario in usuarios:
        usuario.Senha = base64.b64encode(usuario.Senha).decode('utf-8')

    return usuarios

def criar_usuario(usuario: UsuarioInsercaoSchema, db: Session):

    senha_bytes = usuario.Senha.encode('utf-8')

    db_usuario = models.Usuario (        
        Nome = usuario.Nome,
        CPF = usuario.CPF,
        Email= usuario.Email,
        DataNascimento= usuario.DataNascimento,
        DataCriacao= usuario.DataCriacao,
        Sexo= usuario.Sexo,
        Senha= senha_bytes
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    usuario = db.scalar(
        select(models.Usuario).where(models.Usuario.CPF == db_usuario.CPF)
    )

    usuario_schema = user_retorno_schema.UsuarioRetornoSchema(
        Id = usuario.Id,
        Nome = usuario.Nome,
        CPF = usuario.CPF,
        Email= usuario.Email,
        DataNascimento= usuario.DataNascimento,
        DataCriacao= usuario.DataCriacao,
        DataAtualizacao= usuario.DataAtualizacao,
        DataFim= usuario.DataFim,
        Sexo= usuario.Sexo,
        Senha= base64.b64encode(usuario.Senha).decode('utf-8')
    )

    return usuario_schema

def atualizar_usuario(id: int, usuario: UsuarioAtualizacaoSchema, db: Session):
    db_usuario = db.scalar(
                        select(models.Usuario).where(models.Usuario.Id == id)
                    )

    if db_usuario == None:
        raise HTTPException(status_code=404, detail='Usuário não existe')

    senha_bytes = usuario.Senha.encode('utf-8')

    db_usuario.Nome = usuario.Nome
    db_usuario.Senha = senha_bytes
    db_usuario.DataAtualizacao = datetime.now()

    db.commit()
    db.refresh(db_usuario)

    usuario_schema = user_retorno_schema.UsuarioRetornoSchema(
        Id = db_usuario.Id,
        Nome = db_usuario.Nome,
        CPF = db_usuario.CPF,
        Email= db_usuario.Email,
        DataNascimento= db_usuario.DataNascimento,
        DataCriacao= db_usuario.DataCriacao,
        DataAtualizacao= db_usuario.DataAtualizacao,
        DataFim= db_usuario.DataFim,
        Sexo= db_usuario.Sexo,
        Senha= base64.b64encode(db_usuario.Senha).decode('utf-8')
    )

    return usuario_schema

def deletar_usuario(id: int, db: Session):
    db_usuario = db.scalar(
                        select(models.Usuario).where(models.Usuario.Id == id)
                    )

    if db_usuario == None:
        raise HTTPException(status_code=404, detail='Usuário não existe')
    
    db_usuario.DataFim = datetime.now()

    db.commit()
    db.refresh(db_usuario)

    return 1