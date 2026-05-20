# PlanEduca — Sistema de Gerenciamento de Planos de Aula

> Plataforma pedagógica com IA integrada para criação, organização e consulta de planos de aula.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Stack Técnica](#stack-técnica)
- [Funcionalidades](#funcionalidades)
- [Itens Bônus Implementados](#itens-bônus-implementados)
- [Instalação e Execução](#instalação-e-execução)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Endpoints da API](#endpoints-da-api)
- [Testes](#testes)
- [Logs Estruturados](#logs-estruturados)
- [Estrutura do Projeto](#estrutura-do-projeto)

---

## Visão Geral

O **PlanEduca** é uma SPA (Single Page Application) fullstack que permite aos docentes:

- Criar, editar, visualizar e excluir planos de aula com campos ricos
- Usar o **Smart Assist** (botão de IA) para gerar automaticamente conteúdos complementares, tópicos relacionados e 3 tags sugeridas, utilizando a API da Anthropic (Claude Sonnet)
- Filtrar planos por disciplina, tag e data prevista
- Buscar por título com debounce
- Ordenar por título, data de cadastro ou data prevista
- Navegar entre resultados com paginação

---

## Stack Técnica

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.12 + Flask 3.0 |
| ORM | SQLAlchemy + Flask-SQLAlchemy |
| Validação | Marshmallow |
| IA | Anthropic API (claude-sonnet-4) |
| Banco de Dados | SQLite (dev) / PostgreSQL (prod) |
| Frontend | HTML5 + CSS3 + JavaScript vanilla (SPA) |
| Servidor Web | Nginx (proxy reverso + static files) |
| Containerização | Docker + Docker Compose |
| CI | GitHub Actions |
| Logs | structlog (JSON estruturado) |

---

## Funcionalidades

### CRUD de Planos de Aula
- ✅ Listagem com paginação (9 por página)
- ✅ Cadastro e edição com validação de campos
- ✅ Exclusão com confirmação
- ✅ Campos: Título, Objetivo, Ementa, Data Prevista, Disciplina, Conteúdos, Recursos de Apoio, Tags

### Smart Assist (IA)
- ✅ Botão "Gerar Recomendações com IA" no formulário
- ✅ Loading state visual (barra animada + spinner) enquanto a IA processa
- ✅ Preenchimento automático de Conteúdos, Recursos de Apoio e Tags
- ✅ Tratamento de erro com mensagem amigável se a IA falhar ou demorar
- ✅ Prompt de sistema instrui Claude como "Assistente Pedagógico"

### Organização e Consulta
- ✅ Filtro por Disciplina
- ✅ Filtro por Tag
- ✅ Filtro por Data Prevista
- ✅ Busca por Título (com debounce 400ms)
- ✅ Ordenação por Título, Data de Cadastro, Data Prevista
- ✅ Toggle de direção (asc/desc)

---

## Itens Bônus Implementados

### 🏆 Bônus 1 — Integração Contínua (CI) com GitHub Actions

Pipeline configurado em `.github/workflows/ci.yml` que executa automaticamente a cada `push`:

1. **flake8** — linter PEP8
2. **black** — verificação de formatação
3. **pytest** — suite de testes unitários (10 testes cobrindo CRUD, filtros, validação, health check)

```
[CI] push → flake8 → black --check → pytest tests/ -v
```

### 🏆 Bônus 2 — Observabilidade com Logs Estruturados (structlog)

Todos os eventos principais são logados em formato **JSON estruturado**, incluindo:

```json
{"event": "ai_request_completed", "title": "Introdução ao OSPF", "discipline": "Redes", "token_usage": 180, "latency_seconds": 1.4, "model": "claude-sonnet-4", "timestamp": "2025-01-01T12:00:00Z"}
{"event": "lesson_plan_created", "plan_id": 42, "title": "Introdução ao OSPF", "timestamp": "..."}
{"event": "lesson_plans_listed", "page": 1, "total": 15, "filters": {"discipline": "Redes"}, "timestamp": "..."}
{"event": "health_check", "status": "healthy", "db": "healthy", "timestamp": "..."}
```

### 🏆 Bônus 3 — Endpoint de Health Check

```
GET /health
```

Resposta:
```json
{
  "status": "healthy",
  "services": {
    "database": "healthy",
    "api": "healthy"
  }
}
```

O frontend exibe o status em tempo real no rodapé da sidebar (dot verde/vermelho), checando a cada 30 segundos.

### 🏆 Bônus 4 — Containerização completa (Docker + Docker Compose)

```bash
# Subir toda a aplicação com um único comando:
docker-compose up --build
```

Serviços:
- `backend` — Flask via Gunicorn (porta interna 5000), com healthcheck
- `frontend` — Nginx servindo a SPA e fazendo proxy reverso para o backend
- `db_data` — Volume persistente para o SQLite

---

## Instalação e Execução

### Pré-requisitos
- [Docker Desktop](https://docs.docker.com/get-docker/) instalado e rodando
- Uma chave de API da Anthropic: https://console.anthropic.com

### Opção A — Script automático (recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/planeduca.git
cd planeduca

# 2. Rode o script de setup (ele guia tudo)
bash setup.sh
```

O script verifica o Docker, cria o `.env`, pede a chave da API e sobe os containers.

### Opção B — Manual passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/planeduca.git
cd planeduca

# 2. Crie o arquivo de variáveis de ambiente
cp backend/.env.example backend/.env

# 3. Edite e insira sua ANTHROPIC_API_KEY
nano backend/.env
# (ou: code backend/.env  se usar VS Code)

# 4. Suba com um único comando
docker compose up --build

# 5. Acesse no navegador
# http://localhost:3000
```

### Comandos úteis

```bash
make up          # sobe em background
make down        # para tudo
make logs        # logs em tempo real
make logs-backend # só logs do Flask
make test        # roda os testes (sem Docker)
make lint        # roda o flake8
make clean       # remove containers e volumes
```

### Executar sem Docker (desenvolvimento local)

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Crie o .env com sua chave
cp .env.example .env
# Edite e insira ANTHROPIC_API_KEY
# Mude DATABASE_URL para: sqlite:///lesson_plans.db  (3 barras, relativo)

python run.py
# API disponível em http://localhost:5000

# Em outro terminal, sirva o frontend:
cd ../frontend
python -m http.server 8080
# Abra http://localhost:8080
# ATENÇÃO: sem Docker, o frontend chama /api diretamente em localhost:5000
# Edite a linha `const API = '/api'` no index.html para `const API = 'http://localhost:5000/api'`
```

---

## Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `ANTHROPIC_API_KEY` | **Obrigatória.** Chave da API da Anthropic | — |
| `DATABASE_URL` | URL do banco de dados | `sqlite:///lesson_plans.db` |
| `FLASK_ENV` | Ambiente Flask | `development` |
| `SECRET_KEY` | Chave secreta Flask | `dev-secret-key` |
| `LOG_LEVEL` | Nível de log (INFO/DEBUG/WARNING) | `INFO` |

> ⚠️ **NUNCA** commite o arquivo `.env` no Git. Ele está no `.gitignore`.

---

## Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/health` | Health check |
| `GET` | `/api/lesson-plans` | Listar (filtros, busca, paginação, ordenação) |
| `POST` | `/api/lesson-plans` | Criar plano |
| `GET` | `/api/lesson-plans/:id` | Detalhar plano |
| `PUT` | `/api/lesson-plans/:id` | Atualizar plano |
| `DELETE` | `/api/lesson-plans/:id` | Excluir plano |
| `POST` | `/api/lesson-plans/smart-assist` | Gerar recomendações com IA |
| `GET` | `/api/lesson-plans/disciplines` | Listar disciplinas únicas |
| `GET` | `/api/lesson-plans/tags` | Listar tags únicas |

### Parâmetros de query (GET /api/lesson-plans)

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `page` | int | Página (padrão: 1) |
| `per_page` | int | Itens por página (máx: 50) |
| `search` | string | Busca por título |
| `discipline` | string | Filtro por disciplina |
| `tag` | string | Filtro por tag |
| `scheduled_date` | date | Filtro por data (YYYY-MM-DD) |
| `sort_by` | string | `title`, `created_at`, `scheduled_date` |
| `order` | string | `asc` ou `desc` |

---

## Testes

```bash
cd backend
pytest tests/ -v
```

Suite cobre:
- Health check
- Listagem (paginação, filtros, busca)
- CRUD completo
- Validação de campos
- Endpoints de disciplinas e tags

---

## Logs Estruturados

Exemplo de saída de log durante operação do Smart Assist:

```
{"event": "smart_assist_requested", "title": "Introdução ao OSPF", "discipline": "Redes", "level": "info", "timestamp": "2025-01-01T10:00:00.000Z"}
{"event": "ai_request_completed", "title": "Introdução ao OSPF", "discipline": "Redes", "token_usage": 180, "latency_seconds": 1.4, "model": "claude-sonnet-4-20250514", "level": "info", "timestamp": "2025-01-01T10:00:01.400Z"}
```

---

## Estrutura do Projeto

```
planeduca/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask factory
│   │   ├── logger.py            # structlog setup
│   │   ├── models/
│   │   │   └── lesson_plan.py   # SQLAlchemy model
│   │   ├── routes/
│   │   │   ├── health.py        # GET /health
│   │   │   └── lesson_plans.py  # CRUD + smart-assist
│   │   └── services/
│   │       ├── ai_service.py    # Anthropic API
│   │       └── schemas.py       # Marshmallow schemas
│   ├── tests/
│   │   └── test_lesson_plans.py
│   ├── run.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .flake8
│   ├── pyproject.toml
│   └── .env.example
├── frontend/
│   ├── index.html               # SPA completa
│   ├── nginx.conf               # Proxy reverso
│   └── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Decisões Técnicas

- **SQLite** para desenvolvimento por zero-config; basta trocar `DATABASE_URL` para PostgreSQL em produção sem nenhuma mudança de código.
- **Frontend vanilla** (sem React/Vue) para simplicidade no Docker — sem etapa de build, o Nginx serve diretamente o `index.html`.
- **Anthropic Claude Sonnet** como LLM: melhor custo-benefício para geração de conteúdo pedagógico estruturado.
- **structlog** em vez do `logging` padrão para JSON estruturado que integra nativamente com ferramentas como Datadog, CloudWatch e Loki.
- **Gunicorn** com 2 workers em produção (container) e `flask run` em desenvolvimento.
