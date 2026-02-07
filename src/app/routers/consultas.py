from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.consulta import ConsultaCreate, ConsultaUpdate, ConsultaResponse
from app.services.consulta import (
    agendar_consulta,
    listar_consultas,
    buscar_consulta,
    atualizar_consulta,
    cancelar_consulta,
)
from app.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/consultas", tags=["Consultas"])


@router.post("", response_model=ConsultaResponse, status_code=201)
def agendar(
    dados: ConsultaCreate,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return agendar_consulta(db, dados)


@router.get("", response_model=list[ConsultaResponse])
def listar(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    medico_id: int | None = Query(None),
    paciente_id: int | None = Query(None),
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return listar_consultas(db, skip=skip, limit=limit, medico_id=medico_id, paciente_id=paciente_id)


@router.get("/{consulta_id}", response_model=ConsultaResponse)
def detalhe(
    consulta_id: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return buscar_consulta(db, consulta_id)


@router.put("/{consulta_id}", response_model=ConsultaResponse)
def atualizar(
    consulta_id: int,
    dados: ConsultaUpdate,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return atualizar_consulta(db, consulta_id, dados)


@router.patch("/{consulta_id}/cancelar", response_model=ConsultaResponse)
def cancelar(
    consulta_id: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return cancelar_consulta(db, consulta_id)
