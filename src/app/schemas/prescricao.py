from datetime import datetime

from pydantic import BaseModel


class PrescricaoCreate(BaseModel):
    prontuario_id: int
    medicamento: str
    dosagem: str
    frequencia: str
    duracao: str
    observacoes: str | None = None


class PrescricaoResponse(BaseModel):
    id: int
    prontuario_id: int
    medicamento: str
    dosagem: str
    frequencia: str
    duracao: str
    observacoes: str | None
    criado_em: datetime

    model_config = {"from_attributes": True}
