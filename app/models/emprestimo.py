from datetime import date
from sqlalchemy import Date, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.enums import EmprestimoStatus


class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False, index=True)
    exemplar_id: Mapped[int] = mapped_column(ForeignKey("exemplares.id"), nullable=False, index=True)
    data_emprestimo: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    devolucao_prevista: Mapped[date] = mapped_column(Date, nullable=False)
    data_devolucao: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[EmprestimoStatus] = mapped_column(
        SQLEnum(EmprestimoStatus, name="emprestimo_status"),
        nullable=False,
        default=EmprestimoStatus.ATIVO,
        index=True,
    )

    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="emprestimos",
    )

    exemplar: Mapped["Exemplar"] = relationship(
        "Exemplar",
        back_populates="emprestimos",
    )

    multa: Mapped["Multa | None"] = relationship(
        "Multa",
        back_populates="emprestimo",
        uselist=False,
    )
