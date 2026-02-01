from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioLogin, UsuarioResponse, Token
from app.services.auth import registrar_usuario, login
from app.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/singup", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def singup(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return registrar_usuario(db, usuario)


@router.post("/login", response_model=Token)
def login_usuario(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    token = login(db, usuario.email, usuario.senha)
    return Token(access_token=token, token_type="bearer")


@router.get("/me", response_model=UsuarioResponse)
def read_me(usuario: Usuario = Depends(get_current_user)):
    return usuario
