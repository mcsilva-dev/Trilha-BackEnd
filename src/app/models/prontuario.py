from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Prontuario(Base):
    __tablename__ = "prontuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    paciente_id: Mapped[int] = mapped_column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicos.id"), nullable=False)
    consulta_id: Mapped[int] = mapped_column(Integer, ForeignKey("consultas.id"), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    diagnostico: Mapped[str | None] = mapped_column(Text, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    paciente = relationship("Paciente", backref="prontuarios", lazy="joined")
    medico = relationship("Medico", backref="prontuarios", lazy="joined")
    consulta = relationship("Consulta", backref="prontuario", lazy="joined")
