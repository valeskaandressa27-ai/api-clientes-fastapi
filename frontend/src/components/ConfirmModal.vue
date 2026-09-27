<script setup lang="ts">
defineProps<{
  titulo: string;
  texto: string;
  carregando?: boolean;
}>();
const emit = defineEmits<{ confirmar: []; cancelar: [] }>();
</script>

<template>
  <div class="modal-fundo" @click.self="emit('cancelar')">
    <div class="modal" role="dialog" aria-modal="true">
      <h2 class="modal__titulo">{{ titulo }}</h2>
      <p class="modal__texto">{{ texto }}</p>
      <div class="modal__acoes">
        <button class="btn" :disabled="carregando" @click="emit('cancelar')">Cancelar</button>
        <button class="btn btn--perigo" :disabled="carregando" @click="emit('confirmar')">
          {{ carregando ? "Excluindo..." : "Excluir" }}
        </button>
      </div>
    </div>
  </div>
</template>
