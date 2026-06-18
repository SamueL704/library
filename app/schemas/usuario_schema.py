from pydantic import BaseModel, ConfigDict, field_validator


class UsuarioBase(BaseModel):
    nome: str
    email: str

    @field_validator("nome", "email")
    @classmethod
    def campo_nao_pode_ser_vazio(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("campo obrigatório")
        return value.strip()

    @field_validator("email")
    @classmethod
    def email_deve_ser_valido(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("email inválido")
        return value.lower()


class UsuarioCreate(UsuarioBase):
    senha: str

    @field_validator("senha")
    @classmethod
    def senha_nao_pode_ser_vazia(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("senha obrigatória")
        return value


class UsuarioResponse(UsuarioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
