import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    port: 5173,
    proxy: {
      // Em desenvolvimento, o Vite encaminha as chamadas de API para o
      // back-end FastAPI rodando em localhost:8000. Em produção, o
      // front-end é servido pela própria aplicação FastAPI (same-origin),
      // então este proxy não é necessário.
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
