import { createRouter, createWebHistory } from "vue-router";
import { api } from "@/services/api";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/LoginView.vue"),
      meta: { titulo: "Entrar", public: true },
    },
    {
      path: "/",
      name: "dashboard",
      component: () => import("@/views/DashboardView.vue"),
      meta: { titulo: "Dashboard" },
    },
    {
      path: "/clientes",
      name: "clientes",
      component: () => import("@/views/ClientesView.vue"),
      meta: { titulo: "Clientes" },
    },
    {
      path: "/clientes/novo",
      name: "cliente-novo",
      component: () => import("@/views/ClienteFormView.vue"),
      meta: { titulo: "Novo cliente" },
    },
    {
      path: "/clientes/:id",
      name: "cliente-detalhe",
      component: () => import("@/views/ClienteDetalheView.vue"),
      meta: { titulo: "Detalhes do cliente" },
      props: true,
    },
    {
      path: "/clientes/:id/editar",
      name: "cliente-editar",
      component: () => import("@/views/ClienteFormView.vue"),
      meta: { titulo: "Editar cliente" },
      props: true,
    },
    {
      path: "/:pathMatch(.*)*",
      name: "nao-encontrado",
      component: () => import("@/views/NaoEncontradoView.vue"),
      meta: { titulo: "Página não encontrada" },
    },
  ],
});

router.beforeEach(async (to) => {
  if (to.meta.public) return true;
  try {
    await api.auth.me();
    return true;
  } catch {
    return { name: "login", query: { redirect: to.fullPath } };
  }
});

router.afterEach((to) => {
  const titulo = (to.meta.titulo as string | undefined) ?? "Customer Management Dashboard";
  document.title = `${titulo} · Customer Management Dashboard`;
});

export default router;
