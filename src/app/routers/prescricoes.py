from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.prescricao import PrescricaoCreate, PrescricaoResponse
from app.services.prescricao import criar_prescricao, listar_prescricoes_prontuario, buscar_prescricao
from app.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/prescricoes", tags=["Prescrições"])


@router.post("", response_model=PrescricaoResponse, status_code=201)
def criar(
    dados: PrescricaoCreate,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return criar_prescricao(db, dados)


@router.get("/prontuario/{prontuario_id}", response_model=list[PrescricaoResponse])
def listar_por_prontuario(
    prontuario_id: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return listar_prescricoes_prontuario(db, prontuario_id)


@router.get("/{prescricao_id}", response_model=PrescricaoResponse)
def detalhe(
    prescricao_id: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return buscar_prescricao(db, prescricao_id)
