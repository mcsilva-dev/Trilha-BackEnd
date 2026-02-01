from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.utils.security import hash_senha, verificar_senha, criar_token


def registrar_usuario(db: Session, dados: UsuarioCreate) -> Usuario:
    existe = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            datail="Email já cadastrado"
        )
    
    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha=hash_senha(dados.senha),
        tipo_usuario=dados.tipo_usuario
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def login(db: Session, email: str, senha: str) -> str:
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not verificar_senha(senha, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )
    
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo",
        )
    
    token = criar_token({"sub": str(usuario.id)})
    return token
