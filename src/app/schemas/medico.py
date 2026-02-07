from datetime import datetime

from pydantic import BaseModel


class MedicoCreate(BaseModel):
    crm: str
    especialidade: str
    telefone: str | None = None


class MedicoUpdate(BaseModel):
    especialidade: str | None = None
    telefone: str | None = None


class MedicoResponse(BaseModel):
    id: int
    usuario_id: int
    crm: str
    especialidade: str
    telefone: str | None
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}
