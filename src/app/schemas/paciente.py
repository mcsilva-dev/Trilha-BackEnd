from datetime import date, datetime

from pydantic import BaseModel, field_validator


class PacienteCreate(BaseModel):
    cpf: str
    data_nascimento: date
    telefone: str | None = None
    endereco: str | None = None
    tipo_sanguineo: str | None = None
    alergias: str | None = None

    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, v: str) -> str:
        cpf = v.strip().replace(".", "").replace("-", "")
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos")
        return cpf


class PacienteUpdate(BaseModel):
    telefone: str | None = None
    endereco: str | None = None
    tipo_sanguineo: str | None = None
    alergias: str | None = None


class PacienteResponse(BaseModel):
    id: int
    usuario_id: int
    cpf: str
    data_nascimento: date
    telefone: str | None
    endereco: str | None
    tipo_sanguineo: str | None
    alergias: str | None
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}
