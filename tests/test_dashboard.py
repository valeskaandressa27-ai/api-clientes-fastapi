"""Testes automatizados para as métricas do dashboard."""


def test_resumo_dashboard_sem_clientes(client):
    resposta = client.get("/api/dashboard/resumo")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["total_clientes"] == 0
    assert corpo["novos_ultimos_7_dias"] == 0
    assert corpo["novos_ultimos_30_dias"] == 0
    assert corpo["clientes_recentes"] == []
    assert len(corpo["cadastros_por_mes"]) == 6


def test_resumo_dashboard_com_clientes(client, cliente_payload):
    client.post("/api/clientes", json=cliente_payload)
    segundo_payload = {
        "nome": "João Souza",
        "email": "joao.souza@example.com",
        "telefone": "81988887777",
        "cpf": "36847439092",
    }
    client.post("/api/clientes", json=segundo_payload)

    resposta = client.get("/api/dashboard/resumo")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["total_clientes"] == 2
    assert corpo["novos_ultimos_7_dias"] == 2
    assert corpo["novos_ultimos_30_dias"] == 2
    assert len(corpo["clientes_recentes"]) == 2
    total_no_mes_atual = sum(item["quantidade"] for item in corpo["cadastros_por_mes"])
    assert total_no_mes_atual == 2
