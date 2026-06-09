📚 Lesson Plan Manager

Sistema web para gerenciamento de planos de aula com arquitetura frontend + backend desacoplada, integração preparada para IA generativa, Docker Compose e observabilidade.


✨ Visão Geral

O projeto foi desenvolvido com foco em:

organização modular

separação de responsabilidades

integração frontend/backend

experiência do usuário

containerização

observabilidade

preparação para integração com IA

A aplicação permite criar, editar, visualizar e excluir planos de aula de forma organizada e intuitiva.

🚀 Funcionalidades

📖 Gerenciamento de Planos de Aula

Cadastro de planos de aula

Edição de conteúdos

Exclusão de registros

Listagem organizada

Busca e filtros

Interface SPA

🤖 Smart Assist (IA)

A funcionalidade Smart Assist foi implementada utilizando integração preparada para modelos de linguagem através da API da Anthropic.

O fluxo da funcionalidade:

O frontend envia título, disciplina e resumo para o backend

O backend monta um prompt estruturado

O serviço de IA processa as informações

O sistema retorna recomendações pedagógicas estruturadas

As recomendações incluem:

conteúdos complementares

tópicos relacionados

tags sugeridas

recursos de apoio

⚠️ Configuração da IA

Por questões de segurança e custo, o projeto é entregue sem uma chave de API válida configurada.

Para habilitar a funcionalidade:

ANTHROPIC_API_KEY=your_api_key

A integração já está completamente estruturada no backend.

🏗️ Arquitetura do Projeto

lesson-plan-manager/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── schemas.py
│   │   ├── logger.py
│   │   └── __init__.py
│   │
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── index.html
│
├── docker-compose.yml
└── README.md

🧠 Tecnologias Utilizadas

Backend

Python

Flask

SQLAlchemy

Marshmallow

Gunicorn

Frontend

HTML

CSS

JavaScript

SPA Architecture

Infraestrutura

Docker

Docker Compose

Nginx

IA

Anthropic Claude API

🐳 Executando com Docker

Pré-requisitos

Docker

Docker Compose

1. Clone o repositório

git clone <repo-url>

2. Acesse a pasta do projeto

cd lesson-plan-manager

3. Configure o ambiente

Crie o arquivo:

backend/.env

Utilize como base:

ANTHROPIC_API_KEY=
DATABASE_URL=sqlite:////app/instance/lesson_plans.db
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=dev-secret-key
LOG_LEVEL=INFO

4. Execute a aplicação

docker compose up --build

🌐 Acessos

Frontend

http://localhost:3000

Backend

http://localhost:5000

Health Check

http://localhost:5000/health

📡 API

Health Check

GET /health

Resposta:

{
  "status": "healthy"
}

Lesson Plans

Criar plano

POST /api/lesson-plans

Listar planos

GET /api/lesson-plans

Atualizar plano

PUT /api/lesson-plans/{id}

Remover plano

DELETE /api/lesson-plans/{id}

Smart Assist

POST /api/lesson-plans/smart-assist

📋 Observabilidade

A aplicação possui logs estruturados para auxiliar monitoramento e debugging.

Os logs incluem:

requisições HTTP

health checks

eventos do sistema

falhas de integração

status da aplicação

Exemplo:

{
  "status": "healthy",
  "db": "healthy",
  "event": "health_check",
  "level": "info"
}

🔐 Variáveis de Ambiente

Variável

Descrição

ANTHROPIC_API_KEY

Chave da API da Anthropic

DATABASE_URL

URL de conexão com banco

FLASK_ENV

Ambiente Flask

FLASK_DEBUG

Debug Flask

SECRET_KEY

Chave secreta da aplicação

LOG_LEVEL

Nível de logs

🧪 Testes

A aplicação possui estrutura preparada para testes automatizados.

Pasta:

backend/tests

🎥 Demonstração

O vídeo de demonstração apresenta:

interface funcionando

CRUD completo

integração frontend/backend

estrutura do backend

integração preparada para IA

Docker Compose

logs e observabilidade

📌 Melhorias Futuras

autenticação de usuários

paginação avançada

persistência em PostgreSQL

cache

testes automatizados completos

deploy em nuvem

IA totalmente operacional com chave configurada

👨‍💻 Autor

Desenvolvido como solução para desafio técnico de gerenciamento de planos de aula.

✅ Status do Projeto

✅ Frontend funcional

✅ Backend funcional

✅ CRUD completo

✅ Docker Compose

✅ Logs estruturados

✅ Health Check

✅ Integração preparada para IA

✅ Variáveis de ambiente

✅ Arquitetura modular

