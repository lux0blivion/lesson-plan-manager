.PHONY: setup up down logs test lint build clean

## Sobe a aplicação completa (primeira vez: faz o build)
up:
	docker compose up --build -d
	@echo "✅ Rodando em http://localhost:3000"

## Para todos os containers
down:
	docker compose down

## Mostra logs em tempo real
logs:
	docker compose logs -f

## Mostra só logs do backend
logs-backend:
	docker compose logs -f backend

## Reconstrói as imagens do zero
build:
	docker compose build --no-cache

## Roda os testes (sem Docker)
test:
	cd backend && ANTHROPIC_API_KEY=test DATABASE_URL=sqlite:///:memory: pytest tests/ -v

## Roda o linter flake8
lint:
	cd backend && flake8 app/ run.py

## Formata o código com black
format:
	cd backend && black app/ run.py

## Remove containers, volumes e imagens do projeto
clean:
	docker compose down -v --rmi local

## Abre um shell no container do backend (para debug)
shell:
	docker compose exec backend sh

## Exibe o status dos containers
status:
	docker compose ps
