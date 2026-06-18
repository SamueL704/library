from __future__ import annotations

from sqlalchemy import Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ExemplarStatus


class Exemplar(Base):
    __tablename__ = "exemplares"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    livro_id: Mapped[int] = mapped_column(ForeignKey("livros.id"), nullable=False)
    status: Mapped[ExemplarStatus] = mapped_column(
        SQLEnum(ExemplarStatus, name="exemplar_status"),
        nullable=False,
        default=ExemplarStatus.DISPONIVEL,
    )

    livro: Mapped["Livro"] = relationship(
        "Livro",
        back_populates="exemplares",
    )

    emprestimos: Mapped[list["Emprestimo"]] = relationship(
        "Emprestimo",
        back_populates="exemplar",
    )
