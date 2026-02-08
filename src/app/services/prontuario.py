from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.prontuario import Prontuario
from app.models.consulta import Consulta
from app.schemas.prontuario import ProntuarioCreate


def criar_prontuario(db: Session, dados: ProntuarioCreate) -> Prontuario:
    consulta = db.query(Consulta).filter(Consulta.id == dados.consulta_id).first()
    if not consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta não encontrada",
        )

    if consulta.medico_id != dados.medico_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o médico da consulta pode registrar o prontuário",
        )

    prontuario = Prontuario(**dados.model_dump())
    db.add(prontuario)
    db.commit()
    db.refresh(prontuario)
    return prontuario


def listar_prontuarios_paciente(db: Session, paciente_id: int) -> list[Prontuario]:
    return db.query(Prontuario).filter(Prontuario.paciente_id == paciente_id).all()


def buscar_prontuario(db: Session, prontuario_id: int) -> Prontuario:
    prontuario = db.query(Prontuario).filter(Prontuario.id == prontuario_id).first()
    if not prontuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prontuário não encontrado",
        )
    return prontuario
