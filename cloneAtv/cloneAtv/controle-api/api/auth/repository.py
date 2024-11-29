from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..schemas import UserInDB, TokenData
from fastapi import HTTPException, status

# Configurações do JWT
SECRET_KEY = "sua_chave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuração para hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Usuários simulados (em produção, isso viria do banco de dados)
fake_users_db = {
    "user@example.com": UserInDB(
        username="user",
        email="user@example.com",
        hashed_password=pwd_context.hash("senha_segura")
    )
}

def verificar_senha(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def autenticar_usuario(email: str, password: str):
    user = fake_users_db.get(email)
    if not user or not verificar_senha(password, user.hashed_password):
        return None
    return user

def criar_token_jwt(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
