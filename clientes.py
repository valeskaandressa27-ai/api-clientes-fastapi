"""Rotas REST para o recurso Cliente."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.cliente import (
    ClienteCreate,
    ClienteListResponse,
    ClienteResponse,
    ClienteUpdate,
    ErroResponse,
)
from app.services.cliente import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post(
    "",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo cliente",
    responses={409: {"model": ErroResponse, "description": "E-mail ou CPF já cadastrado"}},
)
def criar_cliente(dados: ClienteCreate, db: Session = Depends(get_db)) -> ClienteResponse:
    service = ClienteService(db)
    cliente = service.criar_cliente(dados)
    return ClienteResponse.model_validate(cliente)


@router.get(
    "",
    response_model=ClienteListResponse,
    summary="Listar clientes com paginação e busca",
)
def listar_clientes(
    pagina: int = Query(default=1, ge=1, description="Número da página"),
    tamanho_pagina: int = Query(default=10, ge=1, le=100, description="Itens por página"),
    nome: str | None = Query(default=None, description="Filtrar por nome (parcial)"),
    email: str | None = Query(default=None, description="Filtrar por e-mail (parcial)"),
    db: Session = Depends(get_db),
) -> ClienteListResponse:
    service = ClienteService(db)
    itens, total = service.listar_clientes(pagina, tamanho_pagina, nome, email)
    return ClienteListResponse(
        total=total,
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
        itens=[ClienteResponse.model_validate(item) for item in itens],
    )


@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse,
    summary="Buscar cliente por ID",
    responses={404: {"model": ErroResponse, "description": "Cliente não encontrado"}},
)
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)) -> ClienteResponse:
    service = ClienteService(db)
    cliente = service.obter_cliente(cliente_id)
    return ClienteResponse.model_validate(cliente)


@router.put(
    "/{cliente_id}",
    response_model=ClienteResponse,
    summary="Atualizar um cliente existente",
    responses={
        404: {"model": ErroResponse, "description": "Cliente não encontrado"},
        409: {"model": ErroResponse, "description": "E-mail ou CPF já cadastrado"},
    },
)
def atualizar_cliente(
    cliente_id: int, dados: ClienteUpdate, db: Session = Depends(get_db)
) -> ClienteResponse:
    service = ClienteService(db)
    cliente = service.atualizar_cliente(cliente_id, dados)
    return ClienteResponse.model_validate(cliente)


@router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir um cliente",
    responses={404: {"model": ErroResponse, "description": "Cliente não encontrado"}},
)
def excluir_cliente(cliente_id: int, db: Session = Depends(get_db)) -> None:
    service = ClienteService(db)
    service.excluir_cliente(cliente_id)
