"""Testes do fluxo de autenticação administrativa."""

def test_endpoints_de_dados_exigem_sessao(unauthenticated_client):
    assert unauthenticated_client.get("/api/clientes").status_code == 401
    assert unauthenticated_client.get("/api/dashboard/resumo").status_code == 401


def test_login_com_credenciais_invalidas(unauthenticated_client):
    resposta = unauthenticated_client.post(
        "/api/auth/login",
        json={"username": "usuario-errado", "password": "senha-errada"},
    )
    assert resposta.status_code == 401
    assert "cm_admin_session" not in resposta.cookies


def test_login_valido_emite_cookie_http_only(unauthenticated_client):
    resposta = unauthenticated_client.post(
        "/api/auth/login",
        json={"username": "test-admin", "password": "test-password-for-ci-only"},
    )
    assert resposta.status_code == 200
    set_cookie = resposta.headers["set-cookie"].lower()
    assert "httponly" in set_cookie
    assert "samesite=strict" in set_cookie
    assert unauthenticated_client.get("/api/auth/me").json() == {"authenticated": True}


def test_logout_invalida_cookie(client):
    resposta = client.post("/api/auth/logout")
    assert resposta.status_code == 200
    assert client.get("/api/auth/me").status_code == 401


def test_health_check_permanece_publico(unauthenticated_client):
    resposta = unauthenticated_client.get("/health")
    assert resposta.status_code == 200
