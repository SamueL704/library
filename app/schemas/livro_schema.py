from pydantic import BaseModel, ConfigDict, field_validator


class LivroBase(BaseModel):
    titulo: str
    autor: str
    descricao: str | None = None

    @field_validator("titulo", "autor")
    @classmethod
    def campo_nao_pode_ser_vazio(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("campo obrigatório")
        return value.strip()


class LivroCreate(LivroBase):
    pass


class LivroUpdate(BaseModel):
    titulo: str | None = None
    autor: str | None = None
    descricao: str | None = None

    @field_validator("titulo", "autor")
    @classmethod
    def campo_nao_pode_ser_vazio(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("campo não pode ser vazio")
        return value.strip() if value else value


class LivroResponse(LivroBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
