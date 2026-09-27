"""Schemas Pydantic para entrada e saída de dados de Cliente."""

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

TELEFONE_REGEX = re.compile(r"^\d{10,11}$")


def limpar_digitos(valor: str) -> str:
    return re.sub(r"\D", "", valor or "")


def cpf_e_valido(cpf: str) -> bool:
    """Valida o CPF usando o algoritmo oficial de dígitos verificadores."""
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calcular_digito(cpf_parcial: str) -> int:
        peso = len(cpf_parcial) + 1
        soma = sum(int(d) * (peso - i) for i, d in enumerate(cpf_parcial))
        resto = (soma * 10) % 11
        return 0 if resto == 10 else resto

    digito1 = calcular_digito(cpf[:9])
    digito2 = calcular_digito(cpf[:9] + str(digito1))
    return cpf[-2:] == f"{digito1}{digito2}"


class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    cpf: str

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("nome não pode ser vazio")
        if len(valor) < 2:
            raise ValueError("nome deve ter ao menos 2 caracteres")
        return valor

    @field_validator("telefone")
    @classmethod
    def validar_telefone(cls, valor: str) -> str:
        digitos = limpar_digitos(valor)
        if not TELEFONE_REGEX.match(digitos):
            raise ValueError("telefone deve conter 10 ou 11 dígitos numéricos (com DDD)")
        return digitos

    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, valor: str) -> str:
        digitos = limpar_digitos(valor)
        if not cpf_e_valido(digitos):
            raise ValueError("CPF inválido")
        return digitos


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class ClienteListResponse(BaseModel):
    total: int
    pagina: int
    tamanho_pagina: int
    itens: list[ClienteResponse]


class ErroResponse(BaseModel):
    detail: str
