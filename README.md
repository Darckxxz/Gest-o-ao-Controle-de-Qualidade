# TaskFlow - Sistema de Gerenciamento de Tarefas

> Desenvolvido pela **TechFlow Solutions** para a startup de logística **LogiTrack**

## Objetivo do Projeto

O **TaskFlow** é uma API RESTful de gerenciamento de tarefas que permite à equipe da LogiTrack acompanhar o fluxo de trabalho em tempo real, priorizar tarefas críticas e monitorar o desempenho de cada colaborador. O sistema foi construído seguindo metodologias ágeis e boas práticas de Engenharia de Software.

## Escopo Inicial

O escopo original contemplava:

- CRUD completo de tarefas (Criar, Listar, Atualizar, Deletar)
- Campos de prioridade (`baixa`, `media`, `alta`) e status (`pendente`, `em_progresso`, `concluida`)
- API RESTful com respostas em JSON
- Testes automatizados com Pytest
- Pipeline de integração contínua com GitHub Actions

## Metodologia Adotada

Utilizamos **Kanban** como metodologia ágil principal. O quadro foi organizado nas colunas:

| Coluna | Descrição |
|--------|-----------|
| **A Fazer (To Do)** | Tarefas planejadas ainda não iniciadas |
| **Em Progresso (In Progress)** | Tarefas ativamente em desenvolvimento |
| **Concluído (Done)** | Tarefas finalizadas e validadas |

O Kanban foi escolhido por sua flexibilidade para equipes de tamanho variável e por facilitar a visualização do fluxo de trabalho sem a rigidez de sprints fixos.

## Tecnologias Utilizadas

| Categoria | Tecnologia |
|-----------|-----------|
| Linguagem | Python 3.11 |
| Framework Web | Flask 3.0 |
| Banco de Dados | SQLite (via sqlite3) |
| Testes | Pytest + pytest-cov |
| Linting | Flake8 |
| CI/CD | GitHub Actions |

## Estrutura do Projeto

```
taskflow/
├── src/                        # Código-fonte principal
│   ├── app.py                  # Fábrica da aplicação Flask
│   ├── database.py             # Configuração e conexão com SQLite
│   ├── models/
│   │   └── task.py             # Modelo de dados: Task
│   └── routes/
│       ├── tasks.py            # Endpoints CRUD de tarefas
│       └── auth.py             # Endpoints de autenticação (mudança de escopo)
├── tests/                      # Testes automatizados
│   ├── conftest.py             # Fixtures compartilhadas (banco temporário)
│   ├── test_tasks.py           # Testes de integração (API)
│   └── test_models.py          # Testes unitários (modelo Task)
├── docs/
│   └── parte_teorica.md        # Documento teórico da disciplina
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline GitHub Actions
├── run.py                      # Ponto de entrada da aplicação
├── requirements.txt
├── pytest.ini
└── README.md
```

## Como Executar

### Pré-requisitos

- Python 3.11 ou superior
- pip

### Instalação

```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/taskflow.git
cd taskflow

# 2. Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS

# 3. Instalar dependências
pip install -r requirements.txt
```

### Executar a Aplicação

```bash
python run.py
```

A API ficará disponível em `http://localhost:5000`.

### Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/tasks` | Listar todas as tarefas |
| `GET` | `/api/tasks/<id>` | Buscar tarefa por ID |
| `POST` | `/api/tasks` | Criar nova tarefa |
| `PUT` | `/api/tasks/<id>` | Atualizar tarefa existente |
| `DELETE` | `/api/tasks/<id>` | Remover tarefa |
| `POST` | `/api/auth/registro` | Registrar novo usuário |
| `POST` | `/api/auth/login` | Autenticar usuário |

### Exemplo de Uso

```bash
# Criar uma tarefa
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Revisar rota de entregas", "prioridade": "alta"}'

# Listar tarefas
curl http://localhost:5000/api/tasks

# Atualizar status
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Revisar rota de entregas", "status": "concluida"}'
```

### Executar Testes

```bash
# Testes com detalhamento
pytest tests/ -v

# Testes com cobertura de código
pytest tests/ --cov=src --cov-report=term-missing
```

---

## Mudança de Escopo

### Contexto

Após a conclusão da Sprint 1 (CRUD de tarefas), o cliente **LogiTrack** solicitou uma nova funcionalidade: **sistema de autenticação de usuários**.

### Justificativa

A demanda surgiu de uma necessidade operacional real: colaboradores de diferentes setores (motoristas, despachantes, supervisores) acessavam o sistema sem controle de identidade. Tarefas críticas de logística estavam sendo modificadas por usuários não autorizados, causando inconsistências no fluxo de trabalho.

### O que foi alterado

| Item | Descrição |
|------|-----------|
| Novo módulo | `src/routes/auth.py` com endpoints `/registro` e `/login` |
| Nova tabela | `users` no banco de dados SQLite |
| Kanban | Novo card adicionado: "Implementar autenticação de usuários" |
| README | Esta seção de mudança de escopo |

### Como foi gerenciado

A mudança foi inserida no quadro Kanban como um novo card na coluna "A Fazer", priorizando-a para a Sprint 2. O desenvolvimento da Sprint 1 não foi interrompido — a nova funcionalidade foi trabalhada em paralelo após a entrega do CRUD base.

### Lição aprendida

Projetos ágeis devem acomodar mudanças sem destruir o que já foi construído. O Kanban permitiu visibilidade imediata do novo requisito para toda a equipe, reduzindo retrabalho e falhas de comunicação.
