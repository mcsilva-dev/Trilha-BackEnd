# MER - Modelo Entidade-Relacionamento - SGHSS

```mermaid
erDiagram
    USUARIOS {
        int id PK
        varchar nome
        varchar email UK
        varchar senha
        enum tipo_usuario "paciente | medico | admin"
        boolean ativo
        datetime criado_em
    }

    PACIENTES {
        int id PK
        int usuario_id FK
        varchar cpf UK
        date data_nascimento
        varchar telefone
        varchar endereco
        varchar tipo_sanguineo
        text alergias
        datetime criado_em
        datetime atualizado_em
    }

    MEDICOS {
        int id PK
        int usuario_id FK
        varchar crm UK
        varchar especialidade
        varchar telefone
        datetime criado_em
        datetime atualizado_em
    }

    CONSULTAS {
        int id PK
        int paciente_id FK
        int medico_id FK
        datetime data_hora
        enum status "agendada | realizada | cancelada"
        text observacoes
        datetime criado_em
        datetime atualizado_em
    }

    PRONTUARIOS {
        int id PK
        int paciente_id FK
        int medico_id FK
        int consulta_id FK
        text descricao
        text diagnostico
        datetime criado_em
    }

    PRESCRICOES {
        int id PK
        int prontuario_id FK
        varchar medicamento
        varchar dosagem
        varchar frequencia
        varchar duracao
        text observacoes
        datetime criado_em
    }

    EXAMES {
        int id PK
        int consulta_id FK
        int paciente_id FK
        int medico_id FK
        varchar tipo_exame
        text descricao
        text resultado
        enum status "solicitado | realizado"
        datetime criado_em
    }

    USUARIOS ||--o| PACIENTES : "possui perfil"
    USUARIOS ||--o| MEDICOS : "possui perfil"
    PACIENTES ||--o{ CONSULTAS : "agenda"
    MEDICOS ||--o{ CONSULTAS : "atende"
    CONSULTAS ||--o| PRONTUARIOS : "gera"
    PACIENTES ||--o{ PRONTUARIOS : "historico"
    MEDICOS ||--o{ PRONTUARIOS : "registra"
    PRONTUARIOS ||--o{ PRESCRICOES : "contem"
    CONSULTAS ||--o{ EXAMES : "solicita"
    PACIENTES ||--o{ EXAMES : "realiza"
    MEDICOS ||--o{ EXAMES : "solicita"
```

## Tabelas e Campos

| Tabela | Campos Chave | Descrição |
|---|---|---|
| usuarios | id (PK), email (UK) | Dados de autenticação de todos os usuários |
| pacientes | id (PK), usuario_id (FK), cpf (UK) | Dados clínicos e pessoais do paciente |
| medicos | id (PK), usuario_id (FK), crm (UK) | Dados profissionais do médico |
| consultas | id (PK), paciente_id (FK), medico_id (FK) | Agendamentos de consultas |
| prontuarios | id (PK), paciente_id (FK), medico_id (FK), consulta_id (FK) | Registros clínicos |
| prescricoes | id (PK), prontuario_id (FK) | Prescrições de medicamentos |
| exames | id (PK), consulta_id (FK), paciente_id (FK), medico_id (FK) | Exames solicitados e resultados |
