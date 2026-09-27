"""Camada de serviço: regras de negócio para Cliente."""

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ClienteNaoEncontradoError,
    CpfDuplicadoError,
    EmailDuplicadoError,
)
from app.models.cliente import Cliente
from app.repositories.cliente import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate


class ClienteService:
    def __init__(self, db: Session) -> None:
        self.repo = ClienteRepository(db)

    def criar_cliente(self, dados: ClienteCreate) -> Cliente:
        if self.repo.buscar_por_email(dados.email):
            raise EmailDuplicadoError(f"já existe um cliente com o e-mail '{dados.email}'")
        if self.repo.buscar_por_cpf(dados.cpf):
            raise CpfDuplicadoError(f"já existe um cliente com o CPF '{dados.cpf}'")
        return self.repo.criar(dados)

    def obter_cliente(self, cliente_id: int) -> Cliente:
        cliente = self.repo.buscar_por_id(cliente_id)
        if cliente is None:
            raise ClienteNaoEncontradoError(f"cliente com id {cliente_id} não encontrado")
        return cliente

    def listar_clientes(
        self,
        pagina: int,
        tamanho_pagina: int,
        nome: str | None = None,
        email: str | None = None,
    ) -> tuple[list[Cliente], int]:
        return self.repo.listar(pagina, tamanho_pagina, nome, email)

    def atualizar_cliente(self, cliente_id: int, dados: ClienteUpdate) -> Cliente:
        cliente = self.obter_cliente(cliente_id)

        email_existente = self.repo.buscar_por_email(dados.email, excluir_id=cliente_id)
        if email_existente:
            raise EmailDuplicadoError(f"já existe um cliente com o e-mail '{dados.email}'")

        cpf_existente = self.repo.buscar_por_cpf(dados.cpf, excluir_id=cliente_id)
        if cpf_existente:
            raise CpfDuplicadoError(f"já existe um cliente com o CPF '{dados.cpf}'")

        return self.repo.atualizar(cliente, dados)

    def excluir_cliente(self, cliente_id: int) -> None:
        cliente = self.obter_cliente(cliente_id)
        self.repo.excluir(cliente)
