from datetime import date, datetime
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator


class UsuarioInsercaoSchema(BaseModel):
    CPF: str
    Nome: str
    Email: EmailStr
    DataNascimento: date
    DataCriacao: datetime
    Sexo: str
    Senha: str

    class Config:
        orm_mode = True

    @field_validator('CPF')
    @classmethod
    def validate_cpf(cls, value: str) -> str:
        tamanhoCpf = len(value)

        if (tamanhoCpf != 11):
             raise HTTPException(status_code=422, detail='CPF inválido com menos de 11 caracteres')
        
        if (value.isdigit() is False):
            raise HTTPException(status_code=422, detail='Digite o CPF numérico, sem pontos e traço')
        
        return value
    
    @field_validator('Nome', 'Senha')
    @classmethod
    def validate_nome(cls, value: str) -> str:
        if (value == ""):
            raise HTTPException(status_code=422, detail='Nome ou senha inválida')
        
        return value

class UsuarioAtualizacaoSchema(BaseModel):
    Nome: str
    Senha: str

    @field_validator('Nome', 'Senha')
    @classmethod
    def validate_nome(cls, value: str) -> str:
        if (value == ""):
            raise HTTPException(status_code=422, detail='Nome ou senha inválida')
        
        return value

    class Config:
        orm_mode = True