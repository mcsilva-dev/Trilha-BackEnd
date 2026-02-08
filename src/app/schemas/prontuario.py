from datetime import datetime

from pydantic import BaseModel


class ProntuarioCreate(BaseModel):
    paciente_id: int
    medico_id: int
    consulta_id: int
    descricao: str
    diagnostico: str | None = None


class ProntuarioResponse(BaseModel):
    id: int
    paciente_id: int
    medico_id: int
    consulta_id: int
    descricao: str
    diagnostico: str | None
    criado_em: datetime

    model_config = {"from_attributes": True}
