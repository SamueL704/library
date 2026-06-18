from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)

    emprestimos: Mapped[list["Emprestimo"]] = relationship(
        "Emprestimo",
        back_populates="usuario",
    )

    multas: Mapped[list["Multa"]] = relationship(
        "Multa",
        back_populates="usuario",
    )
