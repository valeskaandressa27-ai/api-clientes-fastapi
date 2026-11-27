<script setup lang="ts">
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import AppSidebar from "@/components/AppSidebar.vue";
import ToastContainer from "@/components/ToastContainer.vue";
import { api } from "@/services/api";

const sidebarAberta = ref(false);
const rota = useRoute();
const router = useRouter();

async function sair() {
  try {
    await api.auth.logout();
  } finally {
    await router.replace({ name: "login" });
  }
}
</script>

<template>
  <router-view v-if="rota.name === 'login'" />

  <div v-else class="app-shell">
    <AppSidebar :aberta="sidebarAberta" @fechar="sidebarAberta = false" />
    <div
      v-if="sidebarAberta"
      class="modal-fundo"
      style="background: rgba(17, 20, 24, 0.35); z-index: 30"
      @click="sidebarAberta = false"
    ></div>

    <div class="conteudo">
      <header class="topbar">
        <div style="display: flex; align-items: center; gap: 12px">
          <button class="topbar__menu-btn" aria-label="Abrir menu" @click="sidebarAberta = true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M4 6h16M4 12h16M4 18h16" stroke-linecap="round" />
            </svg>
          </button>
          <h1 class="topbar__titulo">{{ rota.meta.titulo }}</h1>
        </div>
        <button class="btn btn--texto btn--pequeno" type="button" @click="sair">Sair</button>
      </header>
      <main class="pagina">
        <router-view />
      </main>
    </div>
    <ToastContainer />
  </div>
</template>
