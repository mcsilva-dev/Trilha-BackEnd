# Documentação dos Endpoints - SGHSS API

## Autenticação

### POST /auth/signup
Cadastro de novo usuário no sistema.

**Request Body:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "minhasenha123",
  "tipo_usuario": "paciente"
}
```

**Respostas:**
- `201` - Usuário criado com sucesso
- `400` - Email já cadastrado
- `422` - Dados inválidos

**Response (201):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "tipo_usuario": "paciente",
  "ativo": true,
  "criado_em": "2026-02-26T00:00:00"
}
```

---

### POST /auth/login
Login com email e senha, retorna token JWT.

**Request Body:**
```json
{
  "email": "joao@email.com",
  "senha": "minhasenha123"
}
```

**Respostas:**
- `200` - Login bem-sucedido
- `401` - Email ou senha incorretos
- `403` - Usuário desativado

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

### GET /auth/me
Retorna dados do usuário autenticado.

**Headers:** `Authorization: Bearer <token>`

**Respostas:**
- `200` - Dados do usuário
- `401` - Token inválido ou ausente

---

## Pacientes

> Todos os endpoints requerem autenticação via Bearer Token.

### POST /pacientes
Cadastra perfil de paciente para o usuário autenticado.

**Request Body:**
```json
{
  "cpf": "12345678901",
  "data_nascimento": "1990-05-15",
  "telefone": "11999990000",
  "endereco": "Rua Exemplo, 123",
  "tipo_sanguineo": "O+",
  "alergias": "Nenhuma"
}
```

**Respostas:**
- `201` - Paciente criado
- `400` - CPF já cadastrado / Usuário já tem perfil

---

### GET /pacientes
Lista pacientes com paginação.

**Query Params:** `skip` (default: 0), `limit` (default: 20, max: 100)

**Resposta:** `200` - Lista de pacientes

---

### GET /pacientes/{id}
Busca paciente por ID.

**Respostas:**
- `200` - Dados do paciente
- `404` - Paciente não encontrado

---

### PUT /pacientes/{id}
Atualiza dados do paciente.

**Request Body:**
```json
{
  "telefone": "11888880000",
  "endereco": "Rua Nova, 456",
  "tipo_sanguineo": "A+",
  "alergias": "Dipirona"
}
```

**Respostas:** `200` - Paciente atualizado | `404` - Não encontrado

---

### DELETE /pacientes/{id}
Remove paciente.

**Respostas:** `204` - Removido | `404` - Não encontrado

---

## Médicos

> Todos os endpoints requerem autenticação via Bearer Token.

### POST /medicos
Cadastra perfil de médico para o usuário autenticado.

**Request Body:**
```json
{
  "crm": "CRM/SP 123456",
  "especialidade": "Cardiologia",
  "telefone": "11999990000"
}
```

**Respostas:**
- `201` - Médico criado
- `400` - CRM já cadastrado / Usuário já tem perfil

---

### GET /medicos
Lista médicos com paginação.

**Query Params:** `skip`, `limit`

**Resposta:** `200` - Lista de médicos

---

### GET /medicos/{id}
**Respostas:** `200` - Dados do médico | `404` - Não encontrado

---

### PUT /medicos/{id}
**Request Body:**
```json
{
  "especialidade": "Neurologia",
  "telefone": "11888880000"
}
```

**Respostas:** `200` - Atualizado | `404` - Não encontrado

---

### DELETE /medicos/{id}
**Respostas:** `204` - Removido | `404` - Não encontrado

---

## Consultas

> Todos os endpoints requerem autenticação via Bearer Token.

### POST /consultas
Agenda nova consulta. Verifica conflito de horário (janela de 30 minutos).

**Request Body:**
```json
{
  "paciente_id": 1,
  "medico_id": 1,
  "data_hora": "2026-03-15T10:00:00",
  "observacoes": "Consulta de rotina"
}
```

**Respostas:**
- `201` - Consulta agendada
- `404` - Paciente ou médico não encontrado
- `409` - Conflito de horário

---

### GET /consultas
Lista consultas com filtros opcionais.

**Query Params:** `skip`, `limit`, `medico_id`, `paciente_id`

**Resposta:** `200` - Lista de consultas

---

### GET /consultas/{id}
**Respostas:** `200` - Detalhe | `404` - Não encontrada

---

### PUT /consultas/{id}
Atualiza data/hora ou observações da consulta.

**Request Body:**
```json
{
  "data_hora": "2026-03-16T14:00:00",
  "observacoes": "Reagendada pelo paciente"
}
```

**Respostas:** `200` - Atualizada | `404` - Não encontrada

---

### PATCH /consultas/{id}/cancelar
Cancela uma consulta agendada.

**Respostas:**
- `200` - Consulta cancelada (retorna status "cancelada")
- `400` - Consulta já cancelada
- `404` - Não encontrada

---

## Prontuários

> Todos os endpoints requerem autenticação via Bearer Token.

### POST /prontuarios
Registra prontuário. Apenas o médico da consulta pode registrar.

**Request Body:**
```json
{
  "paciente_id": 1,
  "medico_id": 1,
  "consulta_id": 1,
  "descricao": "Paciente apresenta dor torácica",
  "diagnostico": "Angina estável"
}
```

**Respostas:**
- `201` - Prontuário criado
- `403` - Médico não é o da consulta
- `404` - Consulta não encontrada

---

### GET /prontuarios/paciente/{paciente_id}
Histórico de prontuários do paciente.

**Resposta:** `200` - Lista de prontuários

---

### GET /prontuarios/{id}
**Respostas:** `200` - Detalhe | `404` - Não encontrado

---

## Prescrições

> Todos os endpoints requerem autenticação via Bearer Token.

### POST /prescricoes
Cria prescrição vinculada a um prontuário.

**Request Body:**
```json
{
  "prontuario_id": 1,
  "medicamento": "Ibuprofeno",
  "dosagem": "400mg",
  "frequencia": "8 em 8 horas",
  "duracao": "5 dias",
  "observacoes": "Tomar após refeições"
}
```

**Respostas:** `201` - Criada | `404` - Prontuário não encontrado

---

### GET /prescricoes/prontuario/{prontuario_id}
Lista prescrições de um prontuário.

**Resposta:** `200` - Lista de prescrições

---

### GET /prescricoes/{id}
**Respostas:** `200` - Detalhe | `404` - Não encontrada

---

## Exames

> Todos os endpoints requerem autenticação via Bearer Token.

### POST /exames
Solicita exame vinculado a uma consulta.

**Request Body:**
```json
{
  "consulta_id": 1,
  "paciente_id": 1,
  "medico_id": 1,
  "tipo_exame": "Raio-X Tórax",
  "descricao": "Verificar infiltrado pulmonar"
}
```

**Resposta:** `201` - Exame solicitado (status: "solicitado")

---

### GET /exames/paciente/{paciente_id}
Lista exames do paciente.

**Resposta:** `200` - Lista de exames

---

### GET /exames/{id}
**Respostas:** `200` - Detalhe | `404` - Não encontrado

---

### PUT /exames/{id}
Atualiza resultado e status do exame.

**Request Body:**
```json
{
  "resultado": "85 mg/dL - Normal",
  "status": "realizado"
}
```

**Respostas:** `200` - Atualizado | `404` - Não encontrado
