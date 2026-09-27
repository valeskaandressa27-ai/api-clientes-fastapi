"""Testes automatizados para os endpoints de Cliente."""


def test_criar_cliente_com_dados_validos(client, cliente_payload):
    resposta = client.post("/clientes", json=cliente_payload)

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == cliente_payload["nome"]
    assert corpo["email"] == cliente_payload["email"]
    assert corpo["cpf"] == cliente_payload["cpf"]
    assert "id" in corpo
    assert "created_at" in corpo


def test_criar_cliente_com_dados_invalidos(client, cliente_payload):
    payload_invalido = {**cliente_payload, "cpf": "12345678900", "nome": ""}

    resposta = client.post("/clientes", json=payload_invalido)

    assert resposta.status_code == 422


def test_criar_cliente_com_email_invalido(client, cliente_payload):
    payload_invalido = {**cliente_payload, "email": "nao-e-um-email"}

    resposta = client.post("/clientes", json=payload_invalido)

    assert resposta.status_code == 422


def test_listar_clientes(client, cliente_payload):
    client.post("/clientes", json=cliente_payload)
    segundo_payload = {
        "nome": "João Souza",
        "email": "joao.souza@example.com",
        "telefone": "81988887777",
        "cpf": "36847439092",
    }
    client.post("/clientes", json=segundo_payload)

    resposta = client.get("/clientes")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["total"] == 2
    assert len(corpo["itens"]) == 2


def test_listar_clientes_com_paginacao(client, cliente_payload):
    for i in range(3):
        payload = {
            "nome": f"Cliente {i}",
            "email": f"cliente{i}@example.com",
            "telefone": "81988887777",
            "cpf": ["09476928352", "36847439092", "41258011930"][i],
        }
        client.post("/clientes", json=payload)

    resposta = client.get("/clientes", params={"pagina": 1, "tamanho_pagina": 2})

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["total"] == 3
    assert len(corpo["itens"]) == 2


def test_buscar_cliente_por_id(client, cliente_payload):
    criado = client.post("/clientes", json=cliente_payload).json()

    resposta = client.get(f"/clientes/{criado['id']}")

    assert resposta.status_code == 200
    assert resposta.json()["id"] == criado["id"]


def test_buscar_cliente_inexistente(client):
    resposta = client.get("/clientes/999999")

    assert resposta.status_code == 404


def test_atualizar_cliente(client, cliente_payload):
    criado = client.post("/clientes", json=cliente_payload).json()
    dados_atualizados = {**cliente_payload, "nome": "Maria Silva Atualizada"}

    resposta = client.put(f"/clientes/{criado['id']}", json=dados_atualizados)

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Maria Silva Atualizada"


def test_atualizar_cliente_inexistente(client, cliente_payload):
    resposta = client.put("/clientes/999999", json=cliente_payload)

    assert resposta.status_code == 404


def test_excluir_cliente(client, cliente_payload):
    criado = client.post("/clientes", json=cliente_payload).json()

    resposta = client.delete(f"/clientes/{criado['id']}")
    assert resposta.status_code == 204

    resposta_busca = client.get(f"/clientes/{criado['id']}")
    assert resposta_busca.status_code == 404


def test_excluir_cliente_inexistente(client):
    resposta = client.delete("/clientes/999999")

    assert resposta.status_code == 404


def test_email_duplicado(client, cliente_payload):
    client.post("/clientes", json=cliente_payload)
    segundo_payload = {**cliente_payload, "cpf": "36847439092"}

    resposta = client.post("/clientes", json=segundo_payload)

    assert resposta.status_code == 409


def test_cpf_duplicado(client, cliente_payload):
    client.post("/clientes", json=cliente_payload)
    segundo_payload = {**cliente_payload, "email": "outro@example.com"}

    resposta = client.post("/clientes", json=segundo_payload)

    assert resposta.status_code == 409


def test_health_check(client):
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}
