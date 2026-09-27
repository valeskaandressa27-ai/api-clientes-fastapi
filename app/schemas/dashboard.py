"""Schemas Pydantic para as métricas do dashboard."""

from pydantic import BaseModel

from app.schemas.cliente import ClienteResponse


class CadastrosPorMes(BaseModel):
    mes: str  # formato AAAA-MM
    quantidade: int


class DashboardResumo(BaseModel):
    total_clientes: int
    novos_ultimos_7_dias: int
    novos_ultimos_30_dias: int
    cadastros_por_mes: list[CadastrosPorMes]
    clientes_recentes: list[ClienteResponse]
