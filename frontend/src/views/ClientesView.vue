<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { api } from "@/services/api";
import { ApiError } from "@/types";
import type { Cliente } from "@/types";
import { formatarCpf, formatarData, formatarTelefone, iniciais } from "@/utils/formatadores";
import { useToast } from "@/composables/useToast";
import ConfirmModal from "@/components/ConfirmModal.vue";

const router = useRouter();
const toast = useToast();

const clientes = ref<Cliente[]>([]);
const total = ref(0);
const pagina = ref(1);
const tamanhoPagina = 10;
const busca = ref("");
const carregando = ref(true);
const erro = ref<string | null>(null);

const clienteParaExcluir = ref<Cliente | null>(null);
const excluindo = ref(false);

let temporizadorBusca: ReturnType<typeof setTimeout> | undefined;

async function carregar() {
  carregando.value = true;
  erro.value = null;
  try {
    const resposta = await api.clientes.listar({
      pagina: pagina.value,
      tamanhoPagina,
      nome: busca.value || undefined,
    });
    clientes.value = resposta.itens;
    total.value = resposta.total;
  } catch (e) {
    erro.value = e instanceof ApiError ? e.mensagens().join(" ") : "Erro ao carregar clientes.";
  } finally {
    carregando.value = false;
  }
}

onMounted(carregar);

watch(busca, () => {
  clearTimeout(temporizadorBusca);
  temporizadorBusca = setTimeout(() => {
    pagina.value = 1;
    carregar();
  }, 350);
});

function irParaPagina(novaPagina: number) {
  pagina.value = novaPagina;
  carregar();
}

function totalPaginas(): number {
  return Math.max(Math.ceil(total.value / tamanhoPagina), 1);
}

function abrirDetalhe(cliente: Cliente) {
  router.push(`/clientes/${cliente.id}`);
}

function pedirExclusao(cliente: Cliente) {
  clienteParaExcluir.value = cliente;
}

async function confirmarExclusao() {
  if (!clienteParaExcluir.value) return;
  excluindo.value = true;
  try {
    await api.clientes.excluir(clienteParaExcluir.value.id);
    toast.sucesso(`Cliente "${clienteParaExcluir.value.nome}" excluído com sucesso.`);
    clienteParaExcluir.value = null;
    if (clientes.value.length === 1 && pagina.value > 1) {
      pagina.value -= 1;
    }
    await carregar();
  } catch (e) {
    toast.erro(e instanceof ApiError ? e.mensagens().join(" ") : "Erro ao excluir cliente.");
  } finally {
    excluindo.value = false;
  }
}
</script>

<template>
  <div>
    <div class="barra-ferramentas">
      <div class="barra-ferramentas__busca">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="7" />
          <path d="M21 21l-4.3-4.3" stroke-linecap="round" />
        </svg>
        <input v-model="busca" type="text" placeholder="Buscar por nome..." />
      </div>
      <router-link to="/clientes/novo" class="btn btn--primario">+ Novo cliente</router-link>
    </div>

    <div class="card">
      <div v-if="carregando" class="carregando">
        <span class="spinner"></span>
        Carregando clientes...
      </div>

      <div v-else-if="erro" style="padding: 22px">
        <div class="alerta alerta--erro" style="margin-bottom: 0">{{ erro }}</div>
      </div>

      <div v-else-if="clientes.length === 0" class="estado-vazio">
        <div class="estado-vazio__icone">🔍</div>
        <div class="estado-vazio__titulo">
          {{ busca ? "Nenhum cliente encontrado" : "Nenhum cliente cadastrado" }}
        </div>
        <p>
          {{
            busca
              ? "Tente buscar por outro nome."
              : "Cadastre o primeiro cliente para começar a usar o sistema."
          }}
        </p>
        <router-link v-if="!busca" to="/clientes/novo" class="btn btn--primario" style="margin-top: 14px">
          Novo cliente
        </router-link>
      </div>

      <template v-else>
        <div class="tabela-container">
          <table class="tabela">
            <thead>
              <tr>
                <th>Nome</th>
                <th>E-mail</th>
                <th>Telefone</th>
                <th>CPF</th>
                <th>Cadastrado em</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="cliente in clientes" :key="cliente.id" style="cursor: pointer" @click="abrirDetalhe(cliente)">
                <td data-rotulo="Nome">
                  <span class="linha-cliente">
                    <span class="avatar-iniciais">{{ iniciais(cliente.nome) }}</span>
                    {{ cliente.nome }}
                  </span>
                </td>
                <td data-rotulo="E-mail">{{ cliente.email }}</td>
                <td data-rotulo="Telefone">{{ formatarTelefone(cliente.telefone) }}</td>
                <td data-rotulo="CPF">{{ formatarCpf(cliente.cpf) }}</td>
                <td data-rotulo="Cadastrado em">{{ formatarData(cliente.created_at) }}</td>
                <td @click.stop>
                  <div class="acoes-tabela">
                    <router-link :to="`/clientes/${cliente.id}`" class="btn btn--texto btn--pequeno">
                      Ver
                    </router-link>
                    <router-link :to="`/clientes/${cliente.id}/editar`" class="btn btn--texto btn--pequeno">
                      Editar
                    </router-link>
                    <button class="btn btn--texto btn--pequeno" style="color: var(--cor-erro)" @click="pedirExclusao(cliente)">
                      Excluir
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="paginacao">
          <span>{{ total }} cliente(s) · página {{ pagina }} de {{ totalPaginas() }}</span>
          <div class="paginacao__botoes">
            <button class="btn btn--pequeno" :disabled="pagina <= 1" @click="irParaPagina(pagina - 1)">
              Anterior
            </button>
            <button class="btn btn--pequeno" :disabled="pagina >= totalPaginas()" @click="irParaPagina(pagina + 1)">
              Próxima
            </button>
          </div>
        </div>
      </template>
    </div>

    <ConfirmModal
      v-if="clienteParaExcluir"
      titulo="Excluir cliente"
      :texto="`Tem certeza de que deseja excluir '${clienteParaExcluir.nome}'? Essa ação não pode ser desfeita.`"
      :carregando="excluindo"
      @cancelar="clienteParaExcluir = null"
      @confirmar="confirmarExclusao"
    />
  </div>
</template>
