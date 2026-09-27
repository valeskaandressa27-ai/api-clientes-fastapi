import type {
  Cliente,
  ClienteInput,
  ClienteListResponse,
  DashboardResumo,
} from "@/types";
import { ApiError } from "@/types";

// Em produção, o front-end é servido pela própria aplicação FastAPI, então
// a origem (same-origin) já é suficiente — VITE_API_URL fica vazio.
// Em desenvolvimento, o proxy do Vite encaminha /api para o FastAPI local.
const BASE_URL = (import.meta.env.VITE_API_URL ?? "") + "/api";

async function request<T>(caminho: string, init?: RequestInit): Promise<T> {
  let resposta: Response;
  try {
    resposta = await fetch(`${BASE_URL}${caminho}`, {
      headers: { "Content-Type": "application/json" },
      ...init,
    });
  } catch {
    throw new ApiError(0, "Não foi possível conectar ao servidor. Tente novamente.");
  }

  if (resposta.status === 204) {
    return undefined as T;
  }

  const corpo = await resposta.json().catch(() => null);

  if (!resposta.ok) {
    throw new ApiError(resposta.status, corpo?.detail ?? "Erro inesperado.");
  }

  return corpo as T;
}

export interface ListarClientesParametros {
  pagina?: number;
  tamanhoPagina?: number;
  nome?: string;
  email?: string;
}

export const api = {
  clientes: {
    listar(parametros: ListarClientesParametros = {}): Promise<ClienteListResponse> {
      const query = new URLSearchParams();
      query.set("pagina", String(parametros.pagina ?? 1));
      query.set("tamanho_pagina", String(parametros.tamanhoPagina ?? 10));
      if (parametros.nome) query.set("nome", parametros.nome);
      if (parametros.email) query.set("email", parametros.email);
      return request<ClienteListResponse>(`/clientes?${query.toString()}`);
    },

    obter(id: number): Promise<Cliente> {
      return request<Cliente>(`/clientes/${id}`);
    },

    criar(dados: ClienteInput): Promise<Cliente> {
      return request<Cliente>("/clientes", {
        method: "POST",
        body: JSON.stringify(dados),
      });
    },

    atualizar(id: number, dados: ClienteInput): Promise<Cliente> {
      return request<Cliente>(`/clientes/${id}`, {
        method: "PUT",
        body: JSON.stringify(dados),
      });
    },

    excluir(id: number): Promise<void> {
      return request<void>(`/clientes/${id}`, { method: "DELETE" });
    },
  },

  dashboard: {
    resumo(): Promise<DashboardResumo> {
      return request<DashboardResumo>("/dashboard/resumo");
    },
  },
};
