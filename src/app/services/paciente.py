from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.paciente import Paciente
from app.models.usuario import Usuario
from app.schemas.paciente import PacienteCreate, PacienteUpdate


def criar_paciente(db: Session, usuario: Usuario, dados: PacienteCreate) -> Paciente:
    existe = db.query(Paciente).filter(Paciente.usuario_id == usuario.id).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já possui perfil de paciente",
        )

    cpf_existe = db.query(Paciente).filter(Paciente.cpf == dados.cpf).first()
    if cpf_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado",
        )

    paciente = Paciente(usuario_id=usuario.id, **dados.model_dump())
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente


def listar_pacientes(db: Session, skip: int = 0, limit: int = 20) -> list[Paciente]:
    return db.query(Paciente).offset(skip).limit(limit).all()


def buscar_paciente(db: Session, paciente_id: int) -> Paciente:
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado",
        )
    return paciente


def atualizar_paciente(db: Session, paciente_id: int, dados: PacienteUpdate) -> Paciente:
    paciente = buscar_paciente(db, paciente_id)

    campos = dados.model_dump(exclude_unset=True)
    for campo, valor in campos.items():
        setattr(paciente, campo, valor)

    db.commit()
    db.refresh(paciente)
    return paciente


def remover_paciente(db: Session, paciente_id: int) -> None:
    paciente = buscar_paciente(db, paciente_id)
    db.delete(paciente)
    db.commit()
