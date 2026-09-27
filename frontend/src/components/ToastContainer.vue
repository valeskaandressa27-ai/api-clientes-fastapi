<script setup lang="ts">
import { useToast } from "@/composables/useToast";

const { toasts, remover } = useToast();
</script>

<template>
  <div class="toast-container">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      class="toast"
      :class="toast.tipo === 'sucesso' ? 'toast--sucesso' : 'toast--erro'"
      @click="remover(toast.id)"
    >
      {{ toast.mensagem }}
    </div>
  </div>
</template>
