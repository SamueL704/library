from datetime import date

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.enums import EmprestimoStatus


class EmprestimoCreate(BaseModel):
    usuario_id: int
    exemplar_id: int
    devolucao_prevista: date
    data_emprestimo: date | None = None

    @model_validator(mode="after")
    def validar_datas(self):
        data_base = self.data_emprestimo or date.today()
        if self.devolucao_prevista < data_base:
            raise ValueError("devolucao_prevista não pode ser anterior à data do empréstimo")
        return self


class EmprestimoUpdate(BaseModel):
    data_devolucao: date | None = None
    status: EmprestimoStatus | None = None


class EmprestimoResponse(BaseModel):
    id: int
    usuario_id: int
    exemplar_id: int
    data_emprestimo: date
    devolucao_prevista: date
    data_devolucao: date | None
    status: EmprestimoStatus

    model_config = ConfigDict(from_attributes=True)
