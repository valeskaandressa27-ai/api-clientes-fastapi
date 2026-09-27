"""Camada de serviço: cálculo de métricas agregadas de clientes."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.dashboard import CadastrosPorMes, DashboardResumo
from app.schemas.cliente import ClienteResponse

MESES_HISTORICO = 6
LIMITE_CLIENTES_RECENTES = 5


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def obter_resumo(self) -> DashboardResumo:
        agora = datetime.now(timezone.utc)
        limite_7_dias = agora - timedelta(days=7)
        limite_30_dias = agora - timedelta(days=30)

        total_clientes = self.db.scalar(select(func.count(Cliente.id))) or 0

        novos_7_dias = (
            self.db.scalar(
                select(func.count(Cliente.id)).where(Cliente.created_at >= limite_7_dias)
            )
            or 0
        )

        novos_30_dias = (
            self.db.scalar(
                select(func.count(Cliente.id)).where(Cliente.created_at >= limite_30_dias)
            )
            or 0
        )

        cadastros_por_mes = self._calcular_cadastros_por_mes(agora)

        clientes_recentes = list(
            self.db.execute(
                select(Cliente).order_by(Cliente.created_at.desc()).limit(LIMITE_CLIENTES_RECENTES)
            ).scalars()
        )

        return DashboardResumo(
            total_clientes=total_clientes,
            novos_ultimos_7_dias=novos_7_dias,
            novos_ultimos_30_dias=novos_30_dias,
            cadastros_por_mes=cadastros_por_mes,
            clientes_recentes=[ClienteResponse.model_validate(c) for c in clientes_recentes],
        )

    def _calcular_cadastros_por_mes(self, agora: datetime) -> list[CadastrosPorMes]:
        meses: list[str] = []
        cursor = agora.replace(day=1)
        for _ in range(MESES_HISTORICO):
            meses.append(cursor.strftime("%Y-%m"))
            ano = cursor.year - (1 if cursor.month == 1 else 0)
            mes = 12 if cursor.month == 1 else cursor.month - 1
            cursor = cursor.replace(year=ano, month=mes)
        meses.reverse()

        limite_inicial = agora.replace(day=1) - timedelta(days=30 * (MESES_HISTORICO - 1))
        clientes = self.db.execute(
            select(Cliente.created_at).where(Cliente.created_at >= limite_inicial)
        ).scalars()

        contagem: dict[str, int] = {mes: 0 for mes in meses}
        for created_at in clientes:
            chave = created_at.strftime("%Y-%m")
            if chave in contagem:
                contagem[chave] += 1

        return [CadastrosPorMes(mes=mes, quantidade=contagem[mes]) for mes in meses]
