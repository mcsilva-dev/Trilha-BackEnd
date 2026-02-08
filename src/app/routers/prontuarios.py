from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.prontuario import ProntuarioCreate, ProntuarioResponse
from app.services.prontuario import criar_prontuario, listar_prontuarios_paciente, buscar_prontuario
from app.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/prontuarios", tags=["Prontuários"])


@router.post("", response_model=ProntuarioResponse, status_code=201)
def registrar(
    dados: ProntuarioCreate,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return criar_prontuario(db, dados)


@router.get("/paciente/{paciente_id}", response_model=list[ProntuarioResponse])
def historico(
    paciente_id: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return listar_prontuarios_paciente(db, paciente_id)


@router.get("/{prontuario_id}", response_model=ProntuarioResponse)
def detalhe(
    prontuario_id: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return buscar_prontuario(db, prontuario_id)
