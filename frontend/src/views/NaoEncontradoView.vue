<script setup lang="ts"></script>

<template>
  <div class="card">
    <div class="estado-vazio">
      <div class="estado-vazio__icone">🧭</div>
      <div class="estado-vazio__titulo">Página não encontrada</div>
      <p>O endereço acessado não existe.</p>
      <router-link to="/" class="btn btn--primario" style="margin-top: 14px">
        Voltar ao Dashboard
      </router-link>
    </div>
  </div>
</template>
