<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";
import AppSidebar from "@/components/AppSidebar.vue";
import ToastContainer from "@/components/ToastContainer.vue";

const sidebarAberta = ref(false);
const rota = useRoute();
</script>

<template>
  <div class="app-shell">
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
          <button
            class="topbar__menu-btn"
            aria-label="Abrir menu"
            @click="sidebarAberta = true"
          >
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M4 6h16M4 12h16M4 18h16" stroke-linecap="round" />
            </svg>
          </button>
          <h1 class="topbar__titulo">{{ rota.meta.titulo }}</h1>
        </div>
      </header>

      <main class="pagina">
        <router-view />
      </main>
    </div>

    <ToastContainer />
  </div>
</template>
