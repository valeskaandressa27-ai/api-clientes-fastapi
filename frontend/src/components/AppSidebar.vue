<script setup lang="ts">
defineProps<{ aberta: boolean }>();
const emit = defineEmits<{ fechar: [] }>();
</script>

<template>
  <aside class="sidebar" :class="{ aberta }">
    <div class="sidebar__marca">
      <div class="sidebar__marca-icone">CM</div>
      <div>
        <div class="sidebar__marca-texto">Customer Management</div>
        <div class="sidebar__marca-subtexto">Dashboard</div>
      </div>
    </div>

    <nav class="sidebar__nav">
      <router-link to="/" class="sidebar__link" @click="emit('fechar')">
        <svg class="sidebar__icone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path d="M3 12l9-9 9 9M5 10v10h14V10" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        Dashboard
      </router-link>
      <router-link to="/clientes" class="sidebar__link" @click="emit('fechar')">
        <svg class="sidebar__icone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <circle cx="9" cy="8" r="3.2" />
          <path d="M3.5 19c0-3.3 2.5-5.5 5.5-5.5s5.5 2.2 5.5 5.5" stroke-linecap="round" />
          <circle cx="17" cy="8.5" r="2.4" />
          <path d="M15.8 13.6c2.4.3 4.2 2.3 4.2 5.4" stroke-linecap="round" />
        </svg>
        Clientes
      </router-link>
    </nav>

    <div class="sidebar__rodape">Customer Management Dashboard v1.0</div>
  </aside>
</template>
