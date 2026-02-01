from datetime import datetime 

from pydantic import BaseModel, EmailStr

from app.models.usuario import TipoUsuario


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo_usuario: TipoUsuario.paciente


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo_usuario: TipoUsuario
    ativo: bool
    criado_em: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"