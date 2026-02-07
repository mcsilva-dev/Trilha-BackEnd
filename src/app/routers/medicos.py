from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.medico import MedicoCreate, MedicoUpdate, MedicoResponse
from app.services.medico import (
    criar_medico,
    listar_medicos,
    buscar_medico,
    atualizar_medico,
    remover_medico,
)
from app.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/medicos", tags=["Médicos"])


@router.post("", response_model=MedicoResponse, status_code=201)
def cadastrar_medico(
    dados: MedicoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return criar_medico(db, usuario, dados)


@router.get("", response_model=list[MedicoResponse])
def listar(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return listar_medicos(db, skip=skip, limit=limit)


@router.get("/{medico_id}", response_model=MedicoResponse)
def buscar(
    medico_id: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return buscar_medico(db, medico_id)


@router.put("/{medico_id}", response_model=MedicoResponse)
def atualizar(
    medico_id: int,
    dados: MedicoUpdate,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    return atualizar_medico(db, medico_id, dados)


@router.delete("/{medico_id}", status_code=204)
def deletar(
    medico_id: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(get_current_user),
):
    remover_medico(db, medico_id)
