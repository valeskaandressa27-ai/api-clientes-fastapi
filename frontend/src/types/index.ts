export interface Cliente {
  id: number;
  nome: string;
  email: string;
  telefone: string;
  cpf: string;
  created_at: string;
  updated_at: string;
}

export interface ClienteInput {
  nome: string;
  email: string;
  telefone: string;
  cpf: string;
}

export interface ClienteListResponse {
  total: number;
  pagina: number;
  tamanho_pagina: number;
  itens: Cliente[];
}

export interface CadastroPorMes {
  mes: string;
  quantidade: number;
}

export interface DashboardResumo {
  total_clientes: number;
  novos_ultimos_7_dias: number;
  novos_ultimos_30_dias: number;
  cadastros_por_mes: CadastroPorMes[];
  clientes_recentes: Cliente[];
}

export interface ErroDetalhado {
  detail: string | { msg: string; loc: (string | number)[] }[];
}

export class ApiError extends Error {
  status: number;
  detail: ErroDetalhado["detail"];

  constructor(status: number, detail: ErroDetalhado["detail"]) {
    super(typeof detail === "string" ? detail : "Erro de validação");
    this.status = status;
    this.detail = detail;
  }

  /** Retorna uma lista de mensagens legíveis para exibir ao usuário. */
  mensagens(): string[] {
    if (typeof this.detail === "string") {
      return [this.detail];
    }
    if (Array.isArray(this.detail)) {
      return this.detail.map((item) => item.msg);
    }
    return ["Ocorreu um erro inesperado."];
  }
}
