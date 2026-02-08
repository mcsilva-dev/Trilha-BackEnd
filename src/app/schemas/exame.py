from datetime import datetime

from pydantic import BaseModel

from app.models.exame import StatusExame


class ExameCreate(BaseModel):
    consulta_id: int
    paciente_id: int
    medico_id: int
    tipo_exame: str
    descricao: str | None = None


class ExameUpdate(BaseModel):
    resultado: str | None = None
    status: StatusExame | None = None


class ExameResponse(BaseModel):
    id: int
    consulta_id: int
    paciente_id: int
    medico_id: int
    tipo_exame: str
    descricao: str | None
    resultado: str | None
    status: StatusExame
    criado_em: datetime

    model_config = {"from_attributes": True}
