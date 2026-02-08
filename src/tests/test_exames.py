from datetime import datetime


def _setup_consulta(client, auth_header, db):
    """Helper: cria paciente, médico e consulta."""
    from app.models.paciente import Paciente
    from app.models.medico import Medico
    from app.models.consulta import Consulta
    from app.models.usuario import Usuario
    from app.utils.security import hash_senha

    resp = client.get("/auth/me", headers=auth_header)
    usuario_id = resp.json()["id"]

    paciente = Paciente(
        usuario_id=usuario_id,
        cpf="99988877766",
        data_nascimento=datetime(1985, 6, 20).date(),
    )
    db.add(paciente)

    usuario_medico = Usuario(
        nome="Dra. Lucia",
        email="lucia@email.com",
        senha=hash_senha("123456"),
        tipo_usuario="medico",
    )
    db.add(usuario_medico)
    db.commit()
    db.refresh(usuario_medico)

    medico = Medico(
        usuario_id=usuario_medico.id,
        crm="CRM/SP 333333",
        especialidade="Radiologia",
    )
    db.add(medico)
    db.commit()
    db.refresh(paciente)
    db.refresh(medico)

    consulta = Consulta(
        paciente_id=paciente.id,
        medico_id=medico.id,
        data_hora=datetime(2026, 4, 5, 14, 0),
    )
    db.add(consulta)
    db.commit()
    db.refresh(consulta)

    return paciente, medico, consulta


def test_solicitar_exame_sucesso(client, auth_header, db):
    paciente, medico, consulta = _setup_consulta(client, auth_header, db)

    dados = {
        "consulta_id": consulta.id,
        "paciente_id": paciente.id,
        "medico_id": medico.id,
        "tipo_exame": "Raio-X Tórax",
        "descricao": "Verificar infiltrado pulmonar",
    }
    resp = client.post("/exames", json=dados, headers=auth_header)
    assert resp.status_code == 201
    assert resp.json()["tipo_exame"] == "Raio-X Tórax"
    assert resp.json()["status"] == "solicitado"


def test_listar_exames_paciente(client, auth_header, db):
    paciente, medico, consulta = _setup_consulta(client, auth_header, db)

    dados = {
        "consulta_id": consulta.id,
        "paciente_id": paciente.id,
        "medico_id": medico.id,
        "tipo_exame": "Hemograma",
    }
    client.post("/exames", json=dados, headers=auth_header)

    resp = client.get(f"/exames/paciente/{paciente.id}", headers=auth_header)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_atualizar_resultado_exame(client, auth_header, db):
    paciente, medico, consulta = _setup_consulta(client, auth_header, db)

    dados = {
        "consulta_id": consulta.id,
        "paciente_id": paciente.id,
        "medico_id": medico.id,
        "tipo_exame": "Glicemia",
    }
    resp = client.post("/exames", json=dados, headers=auth_header)
    exame_id = resp.json()["id"]

    resp = client.put(
        f"/exames/{exame_id}",
        json={"resultado": "85 mg/dL - Normal", "status": "realizado"},
        headers=auth_header,
    )
    assert resp.status_code == 200
    assert resp.json()["resultado"] == "85 mg/dL - Normal"
    assert resp.json()["status"] == "realizado"


def test_exame_inexistente(client, auth_header):
    resp = client.get("/exames/9999", headers=auth_header)
    assert resp.status_code == 404
