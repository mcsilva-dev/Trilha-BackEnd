from datetime import datetime


def _setup_prontuario(client, auth_header, db):
    """Helper: cria paciente, médico, consulta e prontuário."""
    from app.models.paciente import Paciente
    from app.models.medico import Medico
    from app.models.consulta import Consulta
    from app.models.prontuario import Prontuario
    from app.models.usuario import Usuario
    from app.utils.security import hash_senha

    resp = client.get("/auth/me", headers=auth_header)
    usuario_id = resp.json()["id"]

    paciente = Paciente(
        usuario_id=usuario_id,
        cpf="11122233344",
        data_nascimento=datetime(1990, 1, 1).date(),
    )
    db.add(paciente)

    usuario_medico = Usuario(
        nome="Dr. Marcos",
        email="marcos@email.com",
        senha=hash_senha("123456"),
        tipo_usuario="medico",
    )
    db.add(usuario_medico)
    db.commit()
    db.refresh(usuario_medico)

    medico = Medico(
        usuario_id=usuario_medico.id,
        crm="CRM/SP 222222",
        especialidade="Ortopedia",
    )
    db.add(medico)
    db.commit()
    db.refresh(paciente)
    db.refresh(medico)

    consulta = Consulta(
        paciente_id=paciente.id,
        medico_id=medico.id,
        data_hora=datetime(2026, 4, 1, 9, 0),
    )
    db.add(consulta)
    db.commit()
    db.refresh(consulta)

    prontuario = Prontuario(
        paciente_id=paciente.id,
        medico_id=medico.id,
        consulta_id=consulta.id,
        descricao="Dor no joelho direito",
    )
    db.add(prontuario)
    db.commit()
    db.refresh(prontuario)

    return paciente, medico, consulta, prontuario


def test_criar_prescricao_sucesso(client, auth_header, db):
    _, _, _, prontuario = _setup_prontuario(client, auth_header, db)

    dados = {
        "prontuario_id": prontuario.id,
        "medicamento": "Ibuprofeno",
        "dosagem": "400mg",
        "frequencia": "8 em 8 horas",
        "duracao": "5 dias",
        "observacoes": "Tomar após refeições",
    }
    resp = client.post("/prescricoes", json=dados, headers=auth_header)
    assert resp.status_code == 201
    assert resp.json()["medicamento"] == "Ibuprofeno"


def test_listar_prescricoes_prontuario(client, auth_header, db):
    _, _, _, prontuario = _setup_prontuario(client, auth_header, db)

    dados = {
        "prontuario_id": prontuario.id,
        "medicamento": "Paracetamol",
        "dosagem": "500mg",
        "frequencia": "6 em 6 horas",
        "duracao": "3 dias",
    }
    client.post("/prescricoes", json=dados, headers=auth_header)

    resp = client.get(f"/prescricoes/prontuario/{prontuario.id}", headers=auth_header)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_prescricao_inexistente(client, auth_header):
    resp = client.get("/prescricoes/9999", headers=auth_header)
    assert resp.status_code == 404
