"""Camada de acesso a dados (repository) para Cliente."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


class ClienteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def criar(self, dados: ClienteCreate) -> Cliente:
        cliente = Cliente(**dados.model_dump())
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def buscar_por_id(self, cliente_id: int) -> Cliente | None:
        return self.db.get(Cliente, cliente_id)

    def buscar_por_email(self, email: str, excluir_id: int | None = None) -> Cliente | None:
        stmt = select(Cliente).where(Cliente.email == email)
        if excluir_id is not None:
            stmt = stmt.where(Cliente.id != excluir_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def buscar_por_cpf(self, cpf: str, excluir_id: int | None = None) -> Cliente | None:
        stmt = select(Cliente).where(Cliente.cpf == cpf)
        if excluir_id is not None:
            stmt = stmt.where(Cliente.id != excluir_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def listar(
        self,
        pagina: int,
        tamanho_pagina: int,
        nome: str | None = None,
        email: str | None = None,
    ) -> tuple[list[Cliente], int]:
        stmt = select(Cliente)
        if nome:
            stmt = stmt.where(Cliente.nome.ilike(f"%{nome}%"))
        if email:
            stmt = stmt.where(Cliente.email.ilike(f"%{email}%"))

        total = len(self.db.execute(stmt).scalars().all())

        stmt = (
            stmt.order_by(Cliente.id)
            .offset((pagina - 1) * tamanho_pagina)
            .limit(tamanho_pagina)
        )
        itens = list(self.db.execute(stmt).scalars().all())
        return itens, total

    def atualizar(self, cliente: Cliente, dados: ClienteUpdate) -> Cliente:
        for campo, valor in dados.model_dump().items():
            setattr(cliente, campo, valor)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def excluir(self, cliente: Cliente) -> None:
        self.db.delete(cliente)
        self.db.commit()
