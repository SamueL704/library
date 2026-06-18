from enum import Enum


class ExemplarStatus(str, Enum):
    DISPONIVEL = "DISPONIVEL"
    EMPRESTADO = "EMPRESTADO"


class EmprestimoStatus(str, Enum):
    ATIVO = "ATIVO"
    ATRASADO = "ATRASADO"
    FINALIZADO = "FINALIZADO"


class MultaStatus(str, Enum):
    PENDENTE = "PENDENTE"
    PAGA = "PAGA"
