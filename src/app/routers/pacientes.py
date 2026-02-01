from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.paciente import PacienteCreate, PacienteUpdate, PacienteResponse
from app.services.paciente import (
    criar_paciente,
    listar_pacientes,
    buscar_paciente,
    atualizar_paciente,
    remover_paciente,
)
from app.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.post("", response_model=PacienteResponse, status_code=201)
def cadastrar_paciente(
    dados: PacienteCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return criar_paciente(db, usuario, dados)


@router.get("", response_model=list[PacienteResponse])
def listar(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return listar_pacientes(db, skip=skip, limit=limit)


@router.get("/{paciente_id}", response_model=PacienteResponse)
def buscar(
    paciente_id: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return buscar_paciente(db, paciente_id)


@router.put("/{paciente_id}", response_model=PacienteResponse)
def atualizar(
    paciente_id: int,
    dados: PacienteUpdate,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return atualizar_paciente(db, paciente_id, dados)


@router.delete("/{paciente_id}", status_code=204)
def deletar(
    paciente_id: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    remover_paciente(db, paciente_id)
