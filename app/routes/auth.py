"""Endpoints de login, consulta de sessão e logout administrativo."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.security import (
    COOKIE_NAME,
    SESSION_MAX_AGE_SECONDS,
    autenticar_credenciais,
    criar_cookie_sessao,
    exigir_admin,
)

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=128)
    password: str = Field(min_length=1, max_length=1024)


@router.post("/login", summary="Iniciar sessão administrativa")
def login(dados: LoginRequest, response: Response) -> dict[str, str]:
    settings = get_settings()
    if not settings.auth_is_configured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Autenticação ainda não configurada no servidor.",
        )
    if not autenticar_credenciais(dados.username, dados.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos.",
        )

    response.set_cookie(
        key=COOKIE_NAME,
        value=criar_cookie_sessao(dados.username),
        max_age=SESSION_MAX_AGE_SECONDS,
        httponly=True,
        secure=settings.is_production,
        samesite="strict",
        path="/",
    )
    return {"message": "Autenticado com sucesso."}


@router.get("/me", summary="Verificar sessão administrativa")
def me(_: Annotated[dict, Depends(exigir_admin)]) -> dict[str, bool]:
    return {"authenticated": True}


@router.post("/logout", summary="Encerrar sessão administrativa")
def logout(response: Response) -> dict[str, str]:
    settings = get_settings()
    response.delete_cookie(
        key=COOKIE_NAME,
        path="/",
        httponly=True,
        secure=settings.is_production,
        samesite="strict",
    )
    return {"message": "Sessão encerrada."}
