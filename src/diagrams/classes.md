# Diagrama de Classes - SGHSS

```mermaid
classDiagram
    class Usuario {
        +int id
        +str nome
        +str email
        +str senha
        +TipoUsuario tipo_usuario
        +bool ativo
        +datetime criado_em
    }

    class Paciente{
        +int id
        +int usuario_id
        +str cpf
        +date data_nascimento
        +str telefone
        +str endereco
        +str tipo_sanguineo
        +str alergias
        +datetime criado_em
        +datetime atualizado_em
    }

    class Medico{
        +int id 
        +int usuario_id
        +str crm
        +str especialidade
        +str telefone
        +datetime criado_em
        +datetime atualizado_em
    }

    class Consulta{
        +int id
        +int paciente_id
        +int medico_id
        +datetime data_hora
        +StatusConsulta status
        +str observacoes
        +datetime criado_em
        +datetime atualizado_em
    }
    class Prontuario{
        +int id
        +int paciente_id
        +int medico_id
        +int consulta_id
        +str descricao
        +str diagnostico
        +datetime criado_em
    }

    class Prescricao{
        +int id
        +int prontuario_id
        +str medicamento
        +str dosagem
        +str frequencia
        +str duracao
        +str observacoes
        +datetime criado_em
    }

    class Exame{
        +int id
        +int consulta_id
        +int paciente_id
        +int medico_id
        +str tipo_exame
        +str descricao
        +str resultado
        +StatusExame status
        +datetime criado_em
    }

    class TipoUsuario{
        <<enumeration>>
        paciente
        medico
        administrador
    }

    class StatusConsulta{
        <<enumeration>>
        agendada
        cancelada
        concluida
    }

    class StatusExame{
        <<enumeration>>
        solicitado
        realizado
    }

    Usuario "1" -- "0..1" Paciente : possui
    Usuario "1" -- "0..1" Medico : possui
    Paciente "1" -- "*" Consulta : agenda
    Medico "1" -- "*" Consulta : atende
    Consulta "1" -- "0..1" Prontuario : gera
    Paciente "1" -- "*" Prontuario : tem historico
    Medico "1" -- "*" Prontuario : registra
    Prontuario "1" -- "*" Prescricao : contem
    Consulta "1" -- "*" Exame : solicita
    Paciente "1" -- "*" Exame : realiza
    Medico "1" -- "*" Exame : solicita
```

## Relacionamentos

| Origem | Destino | Tipo | Descrição |
|---|---|---|---|
| Usuario | Paciente | 1:0..1 | Um usuário pode ter um perfil de paciente |
| Usuario | Medico | 1:0..1 | Um usuário pode ter um perfil de médico |
| Paciente | Consulta | 1:N | Um paciente pode ter várias consultas |
| Medico | Consulta | 1:N | Um médico pode atender várias consultas |
| Consulta | Prontuario | 1:0..1 | Uma consulta pode gerar um prontuário |
| Prontuario | Prescricao | 1:N | Um prontuário pode ter várias prescrições |
| Consulta | Exame | 1:N | Uma consulta pode solicitar vários exames |