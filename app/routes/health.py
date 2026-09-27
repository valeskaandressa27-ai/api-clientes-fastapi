"""Rota de verificação de saúde da aplicação."""

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Verificar status da API")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
