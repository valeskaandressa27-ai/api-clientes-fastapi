<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { api } from "@/services/api";
import { ApiError } from "@/types";
import type { Cliente } from "@/types";
import { formatarCpf, formatarDataHora, formatarTelefone, iniciais } from "@/utils/formatadores";
import { useToast } from "@/composables/useToast";
import ConfirmModal from "@/components/ConfirmModal.vue";

const props = defineProps<{ id: string }>();
const router = useRouter();
const toast = useToast();

const cliente = ref<Cliente | null>(null);
const carregando = ref(true);
const erro = ref<string | null>(null);
const confirmandoExclusao = ref(false);
const excluindo = ref(false);

async function carregar() {
  carregando.value = true;
  erro.value = null;
  try {
    cliente.value = await api.clientes.obter(Number(props.id));
  } catch (e) {
    erro.value =
      e instanceof ApiError
        ? e.status === 404
          ? "Cliente não encontrado."
          : e.mensagens().join(" ")
        : "Erro ao carregar cliente.";
  } finally {
    carregando.value = false;
  }
}

onMounted(carregar);

async function excluir() {
  if (!cliente.value) return;
  excluindo.value = true;
  try {
    await api.clientes.excluir(cliente.value.id);
    toast.sucesso(`Cliente "${cliente.value.nome}" excluído com sucesso.`);
    router.push("/clientes");
  } catch (e) {
    toast.erro(e instanceof ApiError ? e.mensagens().join(" ") : "Erro ao excluir cliente.");
    excluindo.value = false;
    confirmandoExclusao.value = false;
  }
}
</script>

<template>
  <div>
    <router-link to="/clientes" class="btn btn--texto btn--pequeno" style="margin-bottom: 16px; padding-left: 0">
      ← Voltar para clientes
    </router-link>

    <div v-if="carregando" class="carregando">
      <span class="spinner"></span>
      Carregando cliente...
    </div>

    <div v-else-if="erro" class="alerta alerta--erro">{{ erro }}</div>

    <div v-else-if="cliente" class="card">
      <div class="card__cabecalho">
        <div style="display: flex; align-items: center; gap: 14px">
          <span class="avatar-iniciais" style="width: 44px; height: 44px; font-size: 15px">
            {{ iniciais(cliente.nome) }}
          </span>
          <div>
            <h2 style="font-size: 17px">{{ cliente.nome }}</h2>
            <span class="badge badge--info">Cliente #{{ cliente.id }}</span>
          </div>
        </div>
        <div style="display: flex; gap: 8px">
          <router-link :to="`/clientes/${cliente.id}/editar`" class="btn">Editar</router-link>
          <button class="btn btn--perigo" @click="confirmandoExclusao = true">Excluir</button>
        </div>
      </div>

      <div class="card__corpo">
        <div class="grid-detalhe">
          <div class="detalhe-item">
            <div class="detalhe-item__rotulo">E-mail</div>
            <div class="detalhe-item__valor">{{ cliente.email }}</div>
          </div>
          <div class="detalhe-item">
            <div class="detalhe-item__rotulo">Telefone</div>
            <div class="detalhe-item__valor">{{ formatarTelefone(cliente.telefone) }}</div>
          </div>
          <div class="detalhe-item">
            <div class="detalhe-item__rotulo">CPF</div>
            <div class="detalhe-item__valor">{{ formatarCpf(cliente.cpf) }}</div>
          </div>
          <div class="detalhe-item">
            <div class="detalhe-item__rotulo">Cadastrado em</div>
            <div class="detalhe-item__valor">{{ formatarDataHora(cliente.created_at) }}</div>
          </div>
          <div class="detalhe-item">
            <div class="detalhe-item__rotulo">Última atualização</div>
            <div class="detalhe-item__valor">{{ formatarDataHora(cliente.updated_at) }}</div>
          </div>
        </div>
      </div>
    </div>

    <ConfirmModal
      v-if="confirmandoExclusao && cliente"
      titulo="Excluir cliente"
      :texto="`Tem certeza de que deseja excluir '${cliente.nome}'? Essa ação não pode ser desfeita.`"
      :carregando="excluindo"
      @cancelar="confirmandoExclusao = false"
      @confirmar="excluir"
    />
  </div>
</template>
