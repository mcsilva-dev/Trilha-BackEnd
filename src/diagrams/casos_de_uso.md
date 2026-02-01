# Diagrama de Casos de Uso - SGHSS

```mermaid
flowchart LR
    subgraph Atores
        P((Paciente))
        M((Médico))
        A((Administrador))
    end
    
    subgraph Sistema SGHSS
        UC1[Realizar Cadastro]
        UC2[Fazer Login]
        UC3[Agendar Consulta]
        UC4[Cancelar Consulta]
        UC5[Visualizar Consultas]
        UC6[Registrar Prontuário]
        UC7[Visualizar Prontuário]
        UC8[Prescrever Medicamento]
        UC9[Solicitar Exame]
        UC10[Atualizar Resultado de Exame]
        UC11[Gerenciar Usuários]
        UC12[Visualizar Logs de Auditoria]
    end

    P --> UC1
    P --> UC2
    P --> UC3
    P --> UC4
    P --> UC5
    P --> UC7

    M --> UC2
    M --> UC5
    M --> UC6
    M --> UC7
    M --> UC8
    M --> UC9
    M --> UC10

    A --> UC2
    A --> UC11
    A --> UC12
    A --> UC5

    UC3 -.->|include| UC2
    UC6 -.->|include| UC5
```

## Descrição dos Casos de Uso

| Caso de Uso | Descrição |
| --- | --- |
| UC1 | Realizar Cadastro | Paciente | Criar conta no sistema com dados pessoais |
| UC2 | Fazer Login | Todos | Autenticar-se para acessar funcionalidades protegidas |
| UC3 | Agendar Consulta | Paciente | Marcar uma consulta com médico |
| UC4 | Cancelar Consulta | Paciente | Cancelar uma consulta previamente agendada |
| UC5 | Visualizar Consultas | Paciente, Médico, Administrador | Listar consultas agendadas com filtros |
| UC6 | Registrar Prontuário | Médico | Criar registro clínico do paciente após a consulta |
| UC7 | Visualizar Prontuário | Paciente, Médico | Consultar histórico clínico do paciente |
| UC8 | Prescrever Medicamento | Médico | Registrar prescrição vinculada ao prontuario |
| UC9 | Solicitar Exame | Médico | Solicitar exame clínico para o paciente |
| UC10 | Atualizar Resultado de Exame | Médico | Registrar resultado de exame realizado |
| UC11 | Gerenciar Usuários | Administrador | Cadastrar, editar e excluir usuários do sistema |
| UC12 | Visualizar Logs de Auditoria | Administrador | Consultar registros de auditoria do sistema |