from __future__ import annotations

from decimal import Decimal

from sqlalchemy import CheckConstraint, Enum as SQLEnum, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import MultaStatus


class Multa(Base):
    __tablename__ = "multas"

    __table_args__ = (
        CheckConstraint("valor >= 0", name="ck_multas_valor_nao_negativo"),
        UniqueConstraint("emprestimo_id", name="uq_multas_emprestimo_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False, index=True)
    emprestimo_id: Mapped[int] = mapped_column(ForeignKey("emprestimos.id"), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[MultaStatus] = mapped_column(
        SQLEnum(MultaStatus, name="multa_status"),
        nullable=False,
        default=MultaStatus.PENDENTE,
        index=True,
    )

    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="multas",
    )

    emprestimo: Mapped["Emprestimo"] = relationship(
        "Emprestimo",
        back_populates="multa",
    )
