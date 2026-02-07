from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.medico import Medico
from app.models.usuario import Usuario
from app.schemas.medico import MedicoCreate, MedicoUpdate


def criar_medico(db: Session, usuario: Usuario, dados: MedicoCreate) -> Medico:
    existe = db.query(Medico).filter(Medico.usuario_id == usuario.id).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já possui perfil de médico",
        )

    crm_existe = db.query(Medico).filter(Medico.crm == dados.crm).first()
    if crm_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CRM já cadastrado",
        )

    medico = Medico(usuario_id=usuario.id, **dados.model_dump())
    db.add(medico)
    db.commit()
    db.refresh(medico)
    return medico


def listar_medicos(db: Session, skip: int = 0, limit: int = 20) -> list[Medico]:
    return db.query(Medico).offset(skip).limit(limit).all()


def buscar_medico(db: Session, medico_id: int) -> Medico:
    medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Médico não encontrado",
        )
    return medico


def atualizar_medico(db: Session, medico_id: int, dados: MedicoUpdate) -> Medico:
    medico = buscar_medico(db, medico_id)

    campos = dados.model_dump(exclude_unset=True)
    for campo, valor in campos.items():
        setattr(medico, campo, valor)

    db.commit()
    db.refresh(medico)
    return medico


def remover_medico(db: Session, medico_id: int) -> None:
    medico = buscar_medico(db, medico_id)
    db.delete(medico)
    db.commit()
