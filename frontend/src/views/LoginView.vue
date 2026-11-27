<script setup lang="ts">
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { api } from "@/services/api";
import { ApiError } from "@/types";

const route = useRoute();
const router = useRouter();
const username = ref("");
const password = ref("");
const carregando = ref(false);
const erro = ref("");

async function entrar() {
  erro.value = "";
  carregando.value = true;
  try {
    await api.auth.login(username.value.trim(), password.value);
    const destino = typeof route.query.redirect === "string" ? route.query.redirect : "/";
    await router.replace(destino);
  } catch (e) {
    erro.value = e instanceof ApiError
      ? e.mensagens().join(" ")
      : "Não foi possível iniciar a sessão. Tente novamente.";
  } finally {
    carregando.value = false;
  }
}
</script>

<template>
  <main class="login-page">
    <section class="login-card">
      <div class="login-brand">
        <span class="login-brand__icon">CM</span>
        <div>
          <h1>Customer Management</h1>
          <p>Área administrativa</p>
        </div>
      </div>

      <div class="login-heading">
        <h2>Acesse sua conta</h2>
        <p>Entre com suas credenciais administrativas para continuar.</p>
      </div>

      <form @submit.prevent="entrar">
        <label class="campo">
          <span class="campo__rotulo">Usuário</span>
          <input v-model="username" class="campo__input" type="text" autocomplete="username"
                 required maxlength="128" :disabled="carregando" />
        </label>
        <label class="campo">
          <span class="campo__rotulo">Senha</span>
          <input v-model="password" class="campo__input" type="password" autocomplete="current-password"
                 required maxlength="1024" :disabled="carregando" />
        </label>
        <div v-if="erro" class="alerta alerta--erro" role="alert">{{ erro }}</div>
        <button class="btn btn--primario login-submit" type="submit" :disabled="carregando">
          {{ carregando ? "Entrando..." : "Entrar" }}
        </button>
      </form>
      <p class="login-footnote">Sua sessão é protegida por cookie seguro e expira após 8 horas.</p>
    </section>
  </main>
</template>
