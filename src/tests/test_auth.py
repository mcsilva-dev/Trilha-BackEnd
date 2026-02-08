def test_signup_sucesso(client, usuario_dados):
    resp = client.post("/auth/signup", json=usuario_dados)
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == usuario_dados["email"]
    assert data["nome"] == usuario_dados["nome"]
    assert "senha" not in data
    assert "senha_hash" not in data


def test_signup_email_duplicado(client, usuario_dados):
    client.post("/auth/signup", json=usuario_dados)
    resp = client.post("/auth/signup", json=usuario_dados)
    assert resp.status_code == 400
    assert "já cadastrado" in resp.json()["detail"]


def test_login_sucesso(client, usuario_dados):
    client.post("/auth/signup", json=usuario_dados)
    resp = client.post("/auth/login", json={
        "email": usuario_dados["email"],
        "senha": usuario_dados["senha"],
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert resp.json()["token_type"] == "bearer"


def test_login_senha_errada(client, usuario_dados):
    client.post("/auth/signup", json=usuario_dados)
    resp = client.post("/auth/login", json={
        "email": usuario_dados["email"],
        "senha": "senhaerrada",
    })
    assert resp.status_code == 401
    assert "inválidos" in resp.json()["detail"]


def test_me_com_token(client, auth_header):
    resp = client.get("/auth/me", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["email"] == "joao@email.com"


def test_me_sem_token(client):
    resp = client.get("/auth/me")
    assert resp.status_code == 401
