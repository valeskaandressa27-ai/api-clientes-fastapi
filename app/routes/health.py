"""Rota de verificação de saúde da aplicação e do banco de dados."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import get_db

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Verificar API e conexão com o banco")
def health_check(db: Session = Depends(get_db)) -> dict[str, str]:
    """Retorna sucesso somente quando a API e o PostgreSQL respondem."""
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}
