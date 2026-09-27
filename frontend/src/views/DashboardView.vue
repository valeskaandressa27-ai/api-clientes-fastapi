<script setup lang="ts">
import { onMounted, ref } from "vue";
import { api } from "@/services/api";
import { ApiError } from "@/types";
import type { DashboardResumo } from "@/types";
import { formatarData, iniciais, nomeMes } from "@/utils/formatadores";

const resumo = ref<DashboardResumo | null>(null);
const carregando = ref(true);
const erro = ref<string | null>(null);

async function carregar() {
  carregando.value = true;
  erro.value = null;
  try {
    resumo.value = await api.dashboard.resumo();
  } catch (e) {
    erro.value = e instanceof ApiError ? e.mensagens().join(" ") : "Erro ao carregar o dashboard.";
  } finally {
    carregando.value = false;
  }
}

onMounted(carregar);

function alturaBarra(quantidade: number, maximo: number): string {
  if (maximo === 0) return "3px";
  const percentual = Math.max((quantidade / maximo) * 100, quantidade > 0 ? 6 : 0);
  return `${percentual}%`;
}
</script>

<template>
  <div>
    <div v-if="carregando" class="carregando">
      <span class="spinner"></span>
      Carregando métricas...
    </div>

    <div v-else-if="erro" class="alerta alerta--erro">{{ erro }}</div>

    <template v-else-if="resumo">
      <div class="grid-metricas">
        <div class="metrica">
          <div class="metrica__rotulo">Total de clientes</div>
          <div class="metrica__valor">{{ resumo.total_clientes }}</div>
        </div>
        <div class="metrica">
          <div class="metrica__rotulo">Novos nos últimos 7 dias</div>
          <div class="metrica__valor">{{ resumo.novos_ultimos_7_dias }}</div>
        </div>
        <div class="metrica">
          <div class="metrica__rotulo">Novos nos últimos 30 dias</div>
          <div class="metrica__valor">{{ resumo.novos_ultimos_30_dias }}</div>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1.3fr 1fr; gap: 20px" class="grid-dashboard">
        <div class="card">
          <div class="card__cabecalho">
            <h2 style="font-size: 15px">Cadastros nos últimos 6 meses</h2>
          </div>
          <div class="card__corpo">
            <div v-if="resumo.cadastros_por_mes.every((m) => m.quantidade === 0)" class="estado-vazio">
              <div class="estado-vazio__titulo">Sem cadastros no período</div>
              <p>Assim que novos clientes forem cadastrados, o gráfico será atualizado.</p>
            </div>
            <div v-else class="grafico-barras">
              <div v-for="item in resumo.cadastros_por_mes" :key="item.mes" class="grafico-barras__coluna">
                <div
                  class="grafico-barras__barra"
                  :style="{
                    height: alturaBarra(
                      item.quantidade,
                      Math.max(...resumo.cadastros_por_mes.map((m) => m.quantidade))
                    ),
                  }"
                  :title="`${item.quantidade} cadastro(s)`"
                ></div>
                <span class="grafico-barras__rotulo">{{ nomeMes(item.mes) }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card__cabecalho">
            <h2 style="font-size: 15px">Clientes recentes</h2>
            <router-link to="/clientes" class="btn btn--texto btn--pequeno">Ver todos</router-link>
          </div>
          <div class="card__corpo" style="padding: 8px 0">
            <div v-if="resumo.clientes_recentes.length === 0" class="estado-vazio">
              <div class="estado-vazio__icone">👥</div>
              <div class="estado-vazio__titulo">Nenhum cliente cadastrado</div>
              <p>Cadastre o primeiro cliente para começar.</p>
              <router-link to="/clientes/novo" class="btn btn--primario" style="margin-top: 14px">
                Novo cliente
              </router-link>
            </div>
            <router-link
              v-for="cliente in resumo.clientes_recentes"
              :key="cliente.id"
              :to="`/clientes/${cliente.id}`"
              style="display: flex; align-items: center; padding: 12px 22px; border-bottom: 1px solid var(--cor-borda)"
            >
              <span class="avatar-iniciais">{{ iniciais(cliente.nome) }}</span>
              <div style="min-width: 0">
                <div style="font-weight: 600; font-size: 14px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap">
                  {{ cliente.nome }}
                </div>
                <div style="font-size: 12px; color: var(--cor-texto-suave)">
                  Cadastrado em {{ formatarData(cliente.created_at) }}
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
@media (max-width: 860px) {
  .grid-dashboard {
    grid-template-columns: 1fr !important;
  }
}
</style>
