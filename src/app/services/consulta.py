from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.consulta import Consulta, StatusConsulta
from app.models.paciente import Paciente
from app.models.medico import Medico
from app.schemas.consulta import ConsultaCreate, ConsultaUpdate


def _verificar_conflito_horario(db: Session, medico_id: int, data_hora, excluir_id: int | None = None):
    """Verifica se o médico já tem consulta agendada no mesmo horário (janela de 30 min)."""
    inicio = data_hora - timedelta(minutes=30)
    fim = data_hora + timedelta(minutes=30)

    query = db.query(Consulta).filter(
        Consulta.medico_id == medico_id,
        Consulta.data_hora >= inicio,
        Consulta.data_hora <= fim,
        Consulta.status != StatusConsulta.cancelada,
    )
    if excluir_id:
        query = query.filter(Consulta.id != excluir_id)

    if query.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Médico já possui consulta agendada neste horário",
        )


def agendar_consulta(db: Session, dados: ConsultaCreate) -> Consulta:
    paciente = db.query(Paciente).filter(Paciente.id == dados.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")

    medico = db.query(Medico).filter(Medico.id == dados.medico_id).first()
    if not medico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado")

    _verificar_conflito_horario(db, dados.medico_id, dados.data_hora)

    consulta = Consulta(**dados.model_dump())
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta


def listar_consultas(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    medico_id: int | None = None,
    paciente_id: int | None = None,
) -> list[Consulta]:
    query = db.query(Consulta)

    if medico_id:
        query = query.filter(Consulta.medico_id == medico_id)
    if paciente_id:
        query = query.filter(Consulta.paciente_id == paciente_id)

    return query.offset(skip).limit(limit).all()


def buscar_consulta(db: Session, consulta_id: int) -> Consulta:
    consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta não encontrada",
        )
    return consulta


def atualizar_consulta(db: Session, consulta_id: int, dados: ConsultaUpdate) -> Consulta:
    consulta = buscar_consulta(db, consulta_id)

    campos = dados.model_dump(exclude_unset=True)

    if "data_hora" in campos and campos["data_hora"]:
        _verificar_conflito_horario(db, consulta.medico_id, campos["data_hora"], excluir_id=consulta_id)

    for campo, valor in campos.items():
        setattr(consulta, campo, valor)

    db.commit()
    db.refresh(consulta)
    return consulta


def cancelar_consulta(db: Session, consulta_id: int) -> Consulta:
    consulta = buscar_consulta(db, consulta_id)

    if consulta.status == StatusConsulta.cancelada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consulta já está cancelada",
        )

    consulta.status = StatusConsulta.cancelada
    db.commit()
    db.refresh(consulta)
    return consulta
