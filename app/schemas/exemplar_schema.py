from pydantic import BaseModel, ConfigDict

from app.models.enums import ExemplarStatus


class ExemplarCreate(BaseModel):
    livro_id: int
    status: ExemplarStatus = ExemplarStatus.DISPONIVEL


class ExemplarUpdate(BaseModel):
    status: ExemplarStatus


class ExemplarResponse(BaseModel):
    id: int
    livro_id: int
    status: ExemplarStatus

    model_config = ConfigDict(from_attributes=True)
