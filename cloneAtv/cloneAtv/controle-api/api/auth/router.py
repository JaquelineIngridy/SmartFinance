from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .repository import autenticar_usuario, criar_token_jwt
from ..schemas import Token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = autenticar_usuario(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = criar_token_jwt({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
