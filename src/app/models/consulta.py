import enum
from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StatusConsulta(str, enum.Enum):
    agendada = "agendada"
    realizada = "realizada"
    cancelada = "cancelada"


class Consulta(Base):
    __tablename__ = "consultas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    paciente_id: Mapped[int] = mapped_column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicos.id"), nullable=False)
    data_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    status: Mapped[StatusConsulta] = mapped_column(
        Enum(StatusConsulta), nullable=False, default=StatusConsulta.agendada
    )
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    paciente = relationship("Paciente", backref="consultas", lazy="joined")
    medico = relationship("Medico", backref="consultas", lazy="joined")
