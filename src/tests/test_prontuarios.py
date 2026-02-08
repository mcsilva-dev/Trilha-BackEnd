from datetime import datetime


def _setup_consulta(client, auth_header, db):
    from app.models.paciente import Paciente
    from app.models.medico import Medico
    from app.models.consulta import Consulta
    from app.models.usuario import Usuario
    from app.utils.security import hash_senha

    resp = client.get("/auth/me", headers=auth_header)
    usuario_id = resp.json()["id"]

    paciente = Paciente(
        usuario_id=usuario_id,
        cpf="12345678901",
        data_nascimento=datetime(1990, 5, 15).date(),
    )
    db.add(paciente)

    usuario_medico = Usuario(
        nome="Dr. Carlos",
        email="carlos@email.com",
        senha=hash_senha("123456"),
        tipo_usuario="medico",
    )
    db.add(usuario_medico)
    db.commit()
    db.refresh(usuario_medico)

    medico = Medico(
        usuario_id=usuario_medico.id,
        crm="CRM/SP 111111",
        especialidade="Clínico Geral",
    )
    db.add(medico)
    db.commit()
    db.refresh(paciente)
    db.refresh(medico)

    consulta = Consulta(
        paciente_id=paciente.id,
        medico_id=medico.id,
        data_hora=datetime(2026, 3, 20, 10, 0),
    )
    db.add(consulta)
    db.commit()
    db.refresh(consulta)

    return paciente, medico, consulta


def test_criar_prontuario_sucesso(client, auth_header, db):
    paciente, medico, consulta = _setup_consulta(client, auth_header, db)

    dados = {
        "paciente_id": paciente.id,
        "medico_id": medico.id,
        "consulta_id": consulta.id,
        "descricao": "Paciente apresenta dor no peito",
        "diagnostico": "Angina estável",
    }
    resp = client.post("/prontuarios", json=dados, headers=auth_header)
    assert resp.status_code == 201
    assert resp.json()["descricao"] == "Paciente apresenta dor no peito"
    assert resp.json()["diagnostico"] == "Angina estável"


def test_criar_prontuario_medico_errado(client, auth_header, db):
    paciente, medico, consulta = _setup_consulta(client, auth_header, db)

    dados = {
        "paciente_id": paciente.id,
        "medico_id": 9999,
        "consulta_id": consulta.id,
        "descricao": "Teste",
    }
    resp = client.post("/prontuarios", json=dados, headers=auth_header)
    assert resp.status_code == 403
    assert "médico da consulta" in resp.json()["detail"]


def test_historico_paciente(client, auth_header, db):
    paciente, medico, consulta = _setup_consulta(client, auth_header, db)

    dados = {
        "paciente_id": paciente.id,
        "medico_id": medico.id,
        "consulta_id": consulta.id,
        "descricao": "Consulta de rotina",
    }
    client.post("/prontuarios", json=dados, headers=auth_header)

    resp = client.get(f"/prontuarios/paciente/{paciente.id}", headers=auth_header)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_prontuario_inexistente(client, auth_header):
    resp = client.get("/prontuarios/9999", headers=auth_header)
    assert resp.status_code == 404
    assert "não encontrado" in resp.json()["detail"]
