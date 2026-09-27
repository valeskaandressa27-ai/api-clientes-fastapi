import { reactive } from "vue";

export interface Toast {
  id: number;
  tipo: "sucesso" | "erro";
  mensagem: string;
}

const estado = reactive<{ toasts: Toast[] }>({ toasts: [] });
let proximoId = 1;

function remover(id: number) {
  const indice = estado.toasts.findIndex((t) => t.id === id);
  if (indice !== -1) estado.toasts.splice(indice, 1);
}

function exibir(tipo: Toast["tipo"], mensagem: string) {
  const id = proximoId++;
  estado.toasts.push({ id, tipo, mensagem });
  setTimeout(() => remover(id), 4000);
}

export function useToast() {
  return {
    toasts: estado.toasts,
    sucesso: (mensagem: string) => exibir("sucesso", mensagem),
    erro: (mensagem: string) => exibir("erro", mensagem),
    remover,
  };
}
