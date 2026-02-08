import enum
from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StatusExame(str, enum.Enum):
    solicitado = "solicitado"
    realizado = "realizado"


class Exame(Base):
    __tablename__ = "exames"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    consulta_id: Mapped[int] = mapped_column(Integer, ForeignKey("consultas.id"), nullable=False)
    paciente_id: Mapped[int] = mapped_column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicos.id"), nullable=False)
    tipo_exame: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    resultado: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[StatusExame] = mapped_column(
        Enum(StatusExame), nullable=False, default=StatusExame.solicitado
    )
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    consulta = relationship("Consulta", backref="exames", lazy="joined")
    paciente = relationship("Paciente", backref="exames", lazy="joined")
    medico = relationship("Medico", backref="exames", lazy="joined")
