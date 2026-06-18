from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Livro(Base):
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    autor: Mapped[str] = mapped_column(String(120), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)

    exemplares: Mapped[list["Exemplar"]] = relationship(
        "Exemplar",
        back_populates="livro",
    )
