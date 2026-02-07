from datetime import datetime, timezone


def _criar_paciente_e_medico(client, auth_header, db):
    """Helper: cria um paciente e um médico para usar nos testes de consulta."""
    from app.models.paciente import Paciente
    from app.models.medico import Medico
    from app.models.usuario import Usuario
    from app.utils.security import hash_senha

    # Pega o usuario autenticado (criado pela fixture auth_header)
    resp = client.get("/auth/me", headers=auth_header)
    usuario_id = resp.json()["id"]

    # Cria perfil de paciente para o usuario autenticado
    paciente = Paciente(
        usuario_id=usuario_id,
        cpf="12345678901",
        data_nascimento=datetime(1990, 5, 15).date(),
    )
    db.add(paciente)

    # Cria outro usuario como médico
    usuario_medico = Usuario(
        nome="Dra. Ana",
        email="ana@email.com",
        senha=hash_senha("123456"),
        tipo_usuario="medico",
    )
    db.add(usuario_medico)
    db.commit()
    db.refresh(usuario_medico)

    medico = Medico(
        usuario_id=usuario_medico.id,
        crm="CRM/SP 654321",
        especialidade="Cardiologia",
    )
    db.add(medico)
    db.commit()
    db.refresh(paciente)
    db.refresh(medico)

    return paciente, medico


def test_agendar_consulta_sucesso(client, auth_header, db):
    paciente, medico = _criar_paciente_e_medico(client, auth_header, db)

    dados = {
        "paciente_id": paciente.id,
        "medico_id": medico.id,
        "data_hora": "2026-03-15T10:00:00",
        "observacoes": "Consulta de rotina",
    }
    resp = client.post("/consultas", json=dados, headers=auth_header)
    assert resp.status_code == 201
    data = resp.json()
    assert data["paciente_id"] == paciente.id
    assert data["medico_id"] == medico.id
    assert data["status"] == "agendada"


def test_conflito_horario(client, auth_header, db):
    paciente, medico = _criar_paciente_e_medico(client, auth_header, db)

    dados = {
        "paciente_id": paciente.id,
        "medico_id": medico.id,
        "data_hora": "2026-03-15T10:00:00",
    }
    resp = client.post("/consultas", json=dados, headers=auth_header)
    assert resp.status_code == 201

    # Tenta agendar no mesmo horário
    resp = client.post("/consultas", json=dados, headers=auth_header)
    assert resp.status_code == 409
    assert "já possui consulta" in resp.json()["detail"]


def test_cancelar_consulta(client, auth_header, db):
    paciente, medico = _criar_paciente_e_medico(client, auth_header, db)

    dados = {
        "paciente_id": paciente.id,
        "medico_id": medico.id,
        "data_hora": "2026-03-15T14:00:00",
    }
    resp = client.post("/consultas", json=dados, headers=auth_header)
    consulta_id = resp.json()["id"]

    resp = client.patch(f"/consultas/{consulta_id}/cancelar", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelada"


def test_listar_consultas_com_filtro(client, auth_header, db):
    paciente, medico = _criar_paciente_e_medico(client, auth_header, db)

    dados = {
        "paciente_id": paciente.id,
        "medico_id": medico.id,
        "data_hora": "2026-03-16T09:00:00",
    }
    client.post("/consultas", json=dados, headers=auth_header)

    resp = client.get(f"/consultas?medico_id={medico.id}", headers=auth_header)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    resp = client.get(f"/consultas?paciente_id={paciente.id}", headers=auth_header)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_consulta_inexistente(client, auth_header):
    resp = client.get("/consultas/9999", headers=auth_header)
    assert resp.status_code == 404
    assert "não encontrada" in resp.json()["detail"]
