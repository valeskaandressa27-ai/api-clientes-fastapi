export function formatarCpf(cpf: string): string {
  const digitos = cpf.replace(/\D/g, "");
  if (digitos.length !== 11) return cpf;
  return digitos.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");
}

export function formatarTelefone(telefone: string): string {
  const digitos = telefone.replace(/\D/g, "");
  if (digitos.length === 11) {
    return digitos.replace(/(\d{2})(\d{5})(\d{4})/, "($1) $2-$3");
  }
  if (digitos.length === 10) {
    return digitos.replace(/(\d{2})(\d{4})(\d{4})/, "($1) $2-$3");
  }
  return telefone;
}

export function formatarData(iso: string): string {
  const data = new Date(iso);
  return data.toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}

export function formatarDataHora(iso: string): string {
  const data = new Date(iso);
  return data.toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function iniciais(nome: string): string {
  const partes = nome.trim().split(/\s+/);
  const primeira = partes[0]?.[0] ?? "";
  const ultima = partes.length > 1 ? partes[partes.length - 1][0] : "";
  return (primeira + ultima).toUpperCase();
}

export function nomeMes(chave: string): string {
  const [ano, mes] = chave.split("-").map(Number);
  const data = new Date(ano, mes - 1, 1);
  return data.toLocaleDateString("pt-BR", { month: "short" }).replace(".", "");
}
