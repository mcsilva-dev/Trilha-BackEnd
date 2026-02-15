# SGHSS - Sistema de Gestão Hospitalar e de Serviços de Saúde

API Back-end para gerenciamento hospitalar da instituição **VidaPlus**, desenvolvida com Python e FastAPI.

## Tecnologias

- **Python 3.12+**
- **FastAPI** - framework web assíncrono
- **SQLAlchemy** - ORM para acesso ao banco de dados
- **Alembic** - controle de migrations
- **MySQL 8.0** - banco de dados relacional (via Docker)
- **JWT (python-jose + bcrypt)** - autenticação baseada em tokens
- **pytest + httpx** - testes automatizados

## Pré-requisitos

- Python 3.12 ou superior
- Docker e Docker Compose
- Git

## Como Rodar

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd sghss
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` conforme necessário.

### 3. Subir o banco de dados

```bash
docker-compose up -d
```

### 4. Instalar gerenciador de dependências uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | bash # Linux
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" # Windows
```

### 5. Criar ambiente virtual e instalar dependências

```bash
uv venv
source venv/Scripts/activate  # Windows
.\venv\Scripts\activate  # Linux
uv sync
```

### 6. Executar migrations

```bash
alembic upgrade head
```

### 7. Rodar a aplicação

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

A documentação interativa (Swagger) pode ser acessada em `http://localhost:8000/docs`.

## Estrutura do Projeto

```
sghss/
├── app/
│   ├── main.py          # Aplicação FastAPI + error handling + logs
│   ├── config.py        # Configurações (env vars, DB URL, JWT)
│   ├── database.py      # Conexão e sessão do banco
│   ├── models/          # Modelos SQLAlchemy
│   │   ├── usuario.py
│   │   ├── paciente.py
│   │   ├── medico.py
│   │   ├── consulta.py
│   │   ├── prontuario.py
│   │   ├── prescricao.py
│   │   └── exame.py
│   ├── schemas/         # Schemas Pydantic (validação)
│   ├── routers/         # Endpoints da API
│   ├── services/        # Lógica de negócio
│   └── utils/           # Utilitários (JWT, hashing, dependências)
├── tests/               # Testes automatizados (34 testes)
├── alembic/             # Migrations do banco
├── diagramas/           # Diagramas UML (Mermaid)
│   ├── casos_de_uso.md
│   ├── diagrama_classes.md
│   └── mer.md
├── docs/                # Documentação dos endpoints
│   └── endpoints.md
├── docker-compose.yml
└── requirements.txt
```

## Endpoints da API

| Método | Rota                              | Descrição                        |
|--------|-----------------------------------|----------------------------------|
| POST   | /auth/signup                      | Cadastro de usuário              |
| POST   | /auth/login                       | Login (retorna JWT)              |
| GET    | /auth/me                          | Dados do usuário logado          |
| POST   | /pacientes                        | Cadastrar paciente               |
| GET    | /pacientes                        | Listar pacientes                 |
| GET    | /pacientes/{id}                   | Buscar paciente por ID           |
| PUT    | /pacientes/{id}                   | Atualizar paciente               |
| DELETE | /pacientes/{id}                   | Remover paciente                 |
| POST   | /medicos                          | Cadastrar médico                 |
| GET    | /medicos                          | Listar médicos                   |
| GET    | /medicos/{id}                     | Buscar médico por ID             |
| PUT    | /medicos/{id}                     | Atualizar médico                 |
| DELETE | /medicos/{id}                     | Remover médico                   |
| POST   | /consultas                        | Agendar consulta                 |
| GET    | /consultas                        | Listar consultas (com filtros)   |
| GET    | /consultas/{id}                   | Detalhe da consulta              |
| PUT    | /consultas/{id}                   | Atualizar consulta               |
| PATCH  | /consultas/{id}/cancelar          | Cancelar consulta                |
| POST   | /prontuarios                      | Registrar prontuário             |
| GET    | /prontuarios/paciente/{id}        | Histórico do paciente            |
| GET    | /prontuarios/{id}                 | Detalhe do prontuário            |
| POST   | /prescricoes                      | Criar prescrição                 |
| GET    | /prescricoes/prontuario/{id}      | Listar por prontuário            |
| GET    | /prescricoes/{id}                 | Detalhe da prescrição            |
| POST   | /exames                           | Solicitar exame                  |
| GET    | /exames/paciente/{id}             | Listar exames do paciente        |
| PUT    | /exames/{id}                      | Atualizar resultado              |
| GET    | /exames/{id}                      | Detalhe do exame                 |

Documentação detalhada com exemplos de request/response em [docs/endpoints.md](docs/endpoints.md).

## Testes

```bash
pytest -v
```

34 testes automatizados cobrindo todos os módulos:
- Autenticação (signup, login, token)
- CRUD de pacientes, médicos
- Agendamento e cancelamento de consultas
- Prontuários eletrônicos
- Prescrições e exames
