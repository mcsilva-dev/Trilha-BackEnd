from datetime import datetime

from pydantic import BaseModel

from app.models.consulta import StatusConsulta


class ConsultaCreate(BaseModel):
    paciente_id: int
    medico_id: int
    data_hora: datetime
    observacoes: str | None = None


class ConsultaUpdate(BaseModel):
    data_hora: datetime | None = None
    observacoes: str | None = None


class ConsultaResponse(BaseModel):
    id: int
    paciente_id: int
    medico_id: int
    data_hora: datetime
    status: StatusConsulta
    observacoes: str | None
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}
