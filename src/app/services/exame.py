from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.exame import Exame
from app.schemas.exame import ExameCreate, ExameUpdate


def solicitar_exame(db: Session, dados: ExameCreate) -> Exame:
    exame = Exame(**dados.model_dump())
    db.add(exame)
    db.commit()
    db.refresh(exame)
    return exame


def listar_exames_paciente(db: Session, paciente_id: int) -> list[Exame]:
    return db.query(Exame).filter(Exame.paciente_id == paciente_id).all()


def buscar_exame(db: Session, exame_id: int) -> Exame:
    exame = db.query(Exame).filter(Exame.id == exame_id).first()
    if not exame:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exame não encontrado",
        )
    return exame


def atualizar_exame(db: Session, exame_id: int, dados: ExameUpdate) -> Exame:
    exame = buscar_exame(db, exame_id)

    campos = dados.model_dump(exclude_unset=True)
    for campo, valor in campos.items():
        setattr(exame, campo, valor)

    db.commit()
    db.refresh(exame)
    return exame
