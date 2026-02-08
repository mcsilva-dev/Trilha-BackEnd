from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.exame import ExameCreate, ExameUpdate, ExameResponse
from app.services.exame import solicitar_exame, listar_exames_paciente, buscar_exame, atualizar_exame
from app.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/exames", tags=["Exames"])


@router.post("", response_model=ExameResponse, status_code=201)
def solicitar(
    dados: ExameCreate,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return solicitar_exame(db, dados)


@router.get("/paciente/{paciente_id}", response_model=list[ExameResponse])
def listar_por_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return listar_exames_paciente(db, paciente_id)


@router.get("/{exame_id}", response_model=ExameResponse)
def detalhe(
    exame_id: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return buscar_exame(db, exame_id)


@router.put("/{exame_id}", response_model=ExameResponse)
def atualizar_resultado(
    exame_id: int,
    dados: ExameUpdate,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return atualizar_exame(db, exame_id, dados)
