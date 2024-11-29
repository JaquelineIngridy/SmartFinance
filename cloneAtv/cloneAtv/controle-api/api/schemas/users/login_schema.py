from pydantic import BaseModel

class LoginSchema(BaseModel):
    CPF: str
    Senha: str
