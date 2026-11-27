"""Autenticação por sessão assinada em cookie HttpOnly."""

import hmac
from typing import Any

from fastapi import HTTPException, Request, status
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.core.config import get_settings

COOKIE_NAME = "cm_admin_session"
SESSION_MAX_AGE_SECONDS = 8 * 60 * 60


def _serializer() -> URLSafeTimedSerializer:
    settings = get_settings()
    if not settings.auth_is_configured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Autenticação ainda não configurada no servidor.",
        )
    return URLSafeTimedSerializer(settings.auth_secret, salt="customer-management-session")


def autenticar_credenciais(username: str, password: str) -> bool:
    settings = get_settings()
    if not settings.auth_is_configured:
        return False
    usuario_valido = hmac.compare_digest(username.encode(), settings.admin_username.encode())
    senha_valida = hmac.compare_digest(password.encode(), settings.admin_password.encode())
    return usuario_valido and senha_valida


def criar_cookie_sessao(username: str) -> str:
    return _serializer().dumps({"sub": username})


def validar_sessao(request: Request) -> dict[str, Any]:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária.",
        )
    try:
        payload = _serializer().loads(token, max_age=SESSION_MAX_AGE_SECONDS)
    except (BadSignature, SignatureExpired):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessão inválida ou expirada.",
        ) from None

    settings = get_settings()
    if not isinstance(payload, dict) or payload.get("sub") != settings.admin_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessão inválida.",
        )
    return payload


def exigir_admin(request: Request) -> dict[str, Any]:
    """Dependência para proteger endpoints administrativos."""
    return validar_sessao(request)
