from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.prescricao import Prescricao
from app.models.prontuario import Prontuario
from app.schemas.prescricao import PrescricaoCreate


def criar_prescricao(db: Session, dados: PrescricaoCreate) -> Prescricao:
    prontuario = db.query(Prontuario).filter(Prontuario.id == dados.prontuario_id).first()
    if not prontuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prontuário não encontrado",
        )

    prescricao = Prescricao(**dados.model_dump())
    db.add(prescricao)
    db.commit()
    db.refresh(prescricao)
    return prescricao


def listar_prescricoes_prontuario(db: Session, prontuario_id: int) -> list[Prescricao]:
    return db.query(Prescricao).filter(Prescricao.prontuario_id == prontuario_id).all()


def buscar_prescricao(db: Session, prescricao_id: int) -> Prescricao:
    prescricao = db.query(Prescricao).filter(Prescricao.id == prescricao_id).first()
    if not prescricao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescrição não encontrada",
        )
    return prescricao
