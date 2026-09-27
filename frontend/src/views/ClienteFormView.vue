<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { api } from "@/services/api";
import { ApiError } from "@/types";
import type { ClienteInput } from "@/types";
import { useToast } from "@/composables/useToast";

const props = defineProps<{ id?: string }>();
const route = useRoute();
const router = useRouter();
const toast = useToast();

const modoEdicao = computed(() => Boolean(props.id ?? route.params.id));
const idCliente = computed(() => Number(props.id ?? route.params.id));

const form = reactive<ClienteInput>({
  nome: "",
  email: "",
  telefone: "",
  cpf: "",
});

const errosCampo = reactive<Record<string, string>>({});
const erroGeral = ref<string | null>(null);
const carregandoDados = ref(false);
const salvando = ref(false);

onMounted(async () => {
  if (!modoEdicao.value) return;
  carregandoDados.value = true;
  try {
    const cliente = await api.clientes.obter(idCliente.value);
    form.nome = cliente.nome;
    form.email = cliente.email;
    form.telefone = cliente.telefone;
    form.cpf = cliente.cpf;
  } catch (e) {
    erroGeral.value =
      e instanceof ApiError ? e.mensagens().join(" ") : "Erro ao carregar dados do cliente.";
  } finally {
    carregandoDados.value = false;
  }
});

function validarCpfLocal(cpf: string): boolean {
  const digitos = cpf.replace(/\D/g, "");
  if (digitos.length !== 11 || /^(\d)\1{10}$/.test(digitos)) return false;

  const calcularDigito = (parcial: string): number => {
    const peso = parcial.length + 1;
    const soma = parcial
      .split("")
      .reduce((acc, digito, indice) => acc + Number(digito) * (peso - indice), 0);
    const resto = (soma * 10) % 11;
    return resto === 10 ? 0 : resto;
  };

  const digito1 = calcularDigito(digitos.slice(0, 9));
  const digito2 = calcularDigito(digitos.slice(0, 9) + digito1);
  return digitos.slice(-2) === `${digito1}${digito2}`;
}

function validarFormulario(): boolean {
  Object.keys(errosCampo).forEach((chave) => delete errosCampo[chave]);

  if (!form.nome.trim() || form.nome.trim().length < 2) {
    errosCampo.nome = "Informe o nome completo (mínimo 2 caracteres).";
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errosCampo.email = "Informe um e-mail válido.";
  }
  const digitosTelefone = form.telefone.replace(/\D/g, "");
  if (digitosTelefone.length < 10 || digitosTelefone.length > 11) {
    errosCampo.telefone = "Telefone deve ter 10 ou 11 dígitos (com DDD).";
  }
  if (!validarCpfLocal(form.cpf)) {
    errosCampo.cpf = "CPF inválido.";
  }

  return Object.keys(errosCampo).length === 0;
}

async function salvar() {
  erroGeral.value = null;
  if (!validarFormulario()) return;

  salvando.value = true;
  try {
    if (modoEdicao.value) {
      await api.clientes.atualizar(idCliente.value, form);
      toast.sucesso("Cliente atualizado com sucesso.");
      router.push(`/clientes/${idCliente.value}`);
    } else {
      const criado = await api.clientes.criar(form);
      toast.sucesso("Cliente cadastrado com sucesso.");
      router.push(`/clientes/${criado.id}`);
    }
  } catch (e) {
    if (e instanceof ApiError) {
      erroGeral.value = e.mensagens().join(" ");
    } else {
      erroGeral.value = "Não foi possível salvar o cliente. Tente novamente.";
    }
  } finally {
    salvando.value = false;
  }
}
</script>

<template>
  <div>
    <router-link
      :to="modoEdicao ? `/clientes/${idCliente}` : '/clientes'"
      class="btn btn--texto btn--pequeno"
      style="margin-bottom: 16px; padding-left: 0"
    >
      ← Voltar
    </router-link>

    <div class="card" style="max-width: 640px">
      <div class="card__cabecalho">
        <h2 style="font-size: 16px">{{ modoEdicao ? "Editar cliente" : "Novo cliente" }}</h2>
      </div>

      <div v-if="carregandoDados" class="carregando">
        <span class="spinner"></span>
        Carregando dados do cliente...
      </div>

      <form v-else class="card__corpo" @submit.prevent="salvar">
        <div v-if="erroGeral" class="alerta alerta--erro">{{ erroGeral }}</div>

        <div class="grid-formulario">
          <div class="campo" style="grid-column: span 2">
            <label class="campo__rotulo" for="nome">Nome completo</label>
            <input id="nome" v-model="form.nome" class="campo__input" type="text" placeholder="Ex: Maria Silva" />
            <span v-if="errosCampo.nome" class="campo__erro">{{ errosCampo.nome }}</span>
          </div>

          <div class="campo">
            <label class="campo__rotulo" for="email">E-mail</label>
            <input id="email" v-model="form.email" class="campo__input" type="email" placeholder="nome@exemplo.com" />
            <span v-if="errosCampo.email" class="campo__erro">{{ errosCampo.email }}</span>
          </div>

          <div class="campo">
            <label class="campo__rotulo" for="telefone">Telefone</label>
            <input id="telefone" v-model="form.telefone" class="campo__input" type="text" placeholder="(81) 99999-8888" />
            <span v-if="errosCampo.telefone" class="campo__erro">{{ errosCampo.telefone }}</span>
          </div>

          <div class="campo" style="grid-column: span 2">
            <label class="campo__rotulo" for="cpf">CPF</label>
            <input id="cpf" v-model="form.cpf" class="campo__input" type="text" placeholder="000.000.000-00" />
            <span v-if="errosCampo.cpf" class="campo__erro">{{ errosCampo.cpf }}</span>
          </div>
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 6px">
          <router-link :to="modoEdicao ? `/clientes/${idCliente}` : '/clientes'" class="btn">
            Cancelar
          </router-link>
          <button class="btn btn--primario" type="submit" :disabled="salvando">
            {{ salvando ? "Salvando..." : modoEdicao ? "Salvar alterações" : "Cadastrar cliente" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
