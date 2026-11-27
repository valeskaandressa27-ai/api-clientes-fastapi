"""Testes para o endpoint de saúde."""

from app.database.session import get_db


def test_health_check_verifica_banco(client):
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok", "database": "ok"}


def test_health_check_retorna_erro_quando_banco_indisponivel(client):
    def banco_indisponivel():
        raise RuntimeError("database unavailable")
        yield

    client.app.dependency_overrides[get_db] = banco_indisponivel
    try:
        resposta = client.get("/health")
    finally:
        client.app.dependency_overrides.pop(get_db, None)

    assert resposta.status_code == 500
    assert resposta.json() == {"detail": "erro interno do servidor"}
