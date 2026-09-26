"""Aplicação FastAPI — API de Gerenciamento de Clientes."""

import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import (
    ClienteNaoEncontradoError,
    CpfDuplicadoError,
    EmailDuplicadoError,
)
from app.routes import clientes, health

logger = logging.getLogger("api_clientes")

settings = get_settings()

app = FastAPI(
    title="API de Gerenciamento de Clientes",
    description="API REST para cadastro, consulta, atualização e exclusão de clientes.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ClienteNaoEncontradoError)
async def cliente_nao_encontrado_handler(
    request: Request, exc: ClienteNaoEncontradoError
) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


@app.exception_handler(EmailDuplicadoError)
async def email_duplicado_handler(request: Request, exc: EmailDuplicadoError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})


@app.exception_handler(CpfDuplicadoError)
async def cpf_duplicado_handler(request: Request, exc: CpfDuplicadoError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})


@app.exception_handler(Exception)
async def erro_inesperado_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Erro inesperado ao processar %s %s", request.method, request.url)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "erro interno do servidor"},
    )


app.include_router(health.router)
app.include_router(clientes.router)
