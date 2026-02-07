def test_criar_medico_sucesso(client, auth_header):
    dados = {
        "crm": "CRM/SP 123456",
        "especialidade": "Cardiologia",
        "telefone": "11999990000",
    }
    resp = client.post("/medicos", json=dados, headers=auth_header)
    assert resp.status_code == 201
    data = resp.json()
    assert data["crm"] == "CRM/SP 123456"
    assert data["especialidade"] == "Cardiologia"


def test_criar_medico_crm_duplicado(client, auth_header, db):
    from app.models.medico import Medico
    from app.models.usuario import Usuario
    from app.utils.security import hash_senha

    outro = Usuario(
        nome="Dr. Pedro",
        email="pedro@email.com",
        senha_hash=hash_senha("123456"),
        tipo_usuario="medico",
    )
    db.add(outro)
    db.commit()
    db.refresh(outro)

    medico = Medico(
        usuario_id=outro.id,
        crm="CRM/SP 123456",
        especialidade="Ortopedia",
    )
    db.add(medico)
    db.commit()

    dados = {
        "crm": "CRM/SP 123456",
        "especialidade": "Cardiologia",
    }
    resp = client.post("/medicos", json=dados, headers=auth_header)
    assert resp.status_code == 400
    assert "CRM já cadastrado" in resp.json()["detail"]


def test_listar_medicos(client, auth_header):
    dados = {
        "crm": "CRM/SP 123456",
        "especialidade": "Cardiologia",
    }
    client.post("/medicos", json=dados, headers=auth_header)

    resp = client.get("/medicos", headers=auth_header)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_buscar_medico_inexistente(client, auth_header):
    resp = client.get("/medicos/9999", headers=auth_header)
    assert resp.status_code == 404
    assert "não encontrado" in resp.json()["detail"]


def test_atualizar_medico(client, auth_header):
    dados = {
        "crm": "CRM/SP 123456",
        "especialidade": "Cardiologia",
        "telefone": "11999990000",
    }
    resp = client.post("/medicos", json=dados, headers=auth_header)
    medico_id = resp.json()["id"]

    resp = client.put(
        f"/medicos/{medico_id}",
        json={"especialidade": "Neurologia", "telefone": "11888880000"},
        headers=auth_header,
    )
    assert resp.status_code == 200
    assert resp.json()["especialidade"] == "Neurologia"
    assert resp.json()["telefone"] == "11888880000"


def test_deletar_medico(client, auth_header):
    dados = {
        "crm": "CRM/SP 123456",
        "especialidade": "Cardiologia",
    }
    resp = client.post("/medicos", json=dados, headers=auth_header)
    medico_id = resp.json()["id"]

    resp = client.delete(f"/medicos/{medico_id}", headers=auth_header)
    assert resp.status_code == 204

    resp = client.get(f"/medicos/{medico_id}", headers=auth_header)
    assert resp.status_code == 404
