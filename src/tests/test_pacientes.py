def test_criar_paciente_sucesso(client, auth_header):
    dados = {
        "cpf": "12345678901",
        "data_nascimento": "1990-05-15",
        "telefone": "11999990000",
        "endereco": "Rua Teste, 123",
        "tipo_sanguineo": "O+",
        "alergias": "Nenhuma",
    }
    resp = client.post("/pacientes", json=dados, headers=auth_header)
    assert resp.status_code == 201
    data = resp.json()
    assert data["cpf"] == "12345678901"
    assert data["data_nascimento"] == "1990-05-15"
    assert data["telefone"] == "11999990000"


def test_criar_paciente_cpf_duplicado(client, auth_header, db):
    from app.models.paciente import Paciente
    from datetime import date, datetime, timezone

    # Cria um paciente direto no banco com outro usuario
    from app.models.usuario import Usuario
    from app.utils.security import hash_senha

    outro = Usuario(
        nome="Maria",
        email="maria@email.com",
        senha=hash_senha("123456"),
    )
    db.add(outro)
    db.commit()
    db.refresh(outro)

    paciente = Paciente(
        usuario_id=outro.id,
        cpf="12345678901",
        data_nascimento=date(1985, 1, 1),
    )
    db.add(paciente)
    db.commit()

    dados = {
        "cpf": "12345678901",
        "data_nascimento": "1990-05-15",
    }
    resp = client.post("/pacientes", json=dados, headers=auth_header)
    assert resp.status_code == 400
    assert "CPF já cadastrado" in resp.json()["detail"]


def test_listar_pacientes(client, auth_header):
    dados = {
        "cpf": "12345678901",
        "data_nascimento": "1990-05-15",
    }
    client.post("/pacientes", json=dados, headers=auth_header)

    resp = client.get("/pacientes", headers=auth_header)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_buscar_paciente_inexistente(client, auth_header):
    resp = client.get("/pacientes/9999", headers=auth_header)
    assert resp.status_code == 404
    assert "não encontrado" in resp.json()["detail"]


def test_atualizar_paciente(client, auth_header):
    dados = {
        "cpf": "12345678901",
        "data_nascimento": "1990-05-15",
        "telefone": "11999990000",
    }
    resp = client.post("/pacientes", json=dados, headers=auth_header)
    paciente_id = resp.json()["id"]

    resp = client.put(
        f"/pacientes/{paciente_id}",
        json={"telefone": "11888880000", "endereco": "Rua Nova, 456"},
        headers=auth_header,
    )
    assert resp.status_code == 200
    assert resp.json()["telefone"] == "11888880000"
    assert resp.json()["endereco"] == "Rua Nova, 456"


def test_deletar_paciente(client, auth_header):
    dados = {
        "cpf": "12345678901",
        "data_nascimento": "1990-05-15",
    }
    resp = client.post("/pacientes", json=dados, headers=auth_header)
    paciente_id = resp.json()["id"]

    resp = client.delete(f"/pacientes/{paciente_id}", headers=auth_header)
    assert resp.status_code == 204

    resp = client.get(f"/pacientes/{paciente_id}", headers=auth_header)
    assert resp.status_code == 404
