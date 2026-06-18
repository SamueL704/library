from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator

from app.models.enums import MultaStatus


class MultaCreate(BaseModel):
    usuario_id: int
    emprestimo_id: int
    valor: Decimal
    status: MultaStatus = MultaStatus.PENDENTE

    @field_validator("valor")
    @classmethod
    def valor_nao_pode_ser_negativo(cls, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError("valor da multa não pode ser negativo")
        return value


class MultaUpdate(BaseModel):
    status: MultaStatus


class MultaResponse(BaseModel):
    id: int
    usuario_id: int
    emprestimo_id: int
    valor: Decimal
    status: MultaStatus

    model_config = ConfigDict(from_attributes=True)
