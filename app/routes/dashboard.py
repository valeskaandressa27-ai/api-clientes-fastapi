"""Rota com métricas agregadas para o Dashboard."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.dashboard import DashboardResumo
from app.services.dashboard import DashboardService

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get(
    "/resumo",
    response_model=DashboardResumo,
    summary="Obter métricas resumidas para o dashboard",
)
def obter_resumo(db: Session = Depends(get_db)) -> DashboardResumo:
    service = DashboardService(db)
    return service.obter_resumo()
