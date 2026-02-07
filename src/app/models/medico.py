from datetime import datetime, timezone

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Medico(Base):
    __tablename__ = "medicos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    crm: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    especialidade: Mapped[str] = mapped_column(String(100), nullable=False)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    usuario = relationship("Usuario", backref="medico", lazy="joined")
