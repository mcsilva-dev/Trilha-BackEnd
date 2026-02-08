from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Prescricao(Base):
    __tablename__ = "prescricoes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    prontuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("prontuarios.id"), nullable=False)
    medicamento: Mapped[str] = mapped_column(String(200), nullable=False)
    dosagem: Mapped[str] = mapped_column(String(100), nullable=False)
    frequencia: Mapped[str] = mapped_column(String(100), nullable=False)
    duracao: Mapped[str] = mapped_column(String(100), nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    prontuario = relationship("Prontuario", backref="prescricoes", lazy="joined")
