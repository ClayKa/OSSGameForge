# OSSGameForge Makefile
# Common development tasks

.PHONY: help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install
install: ## Install all dependencies
	cd backend && pip install -r requirements-dev.txt
	cd frontend && npm install
	pre-commit install

.PHONY: build
build: ## Build Docker images
	docker-compose build

.PHONY: up
up: ## Start all services
	docker-compose up -d

.PHONY: down
down: ## Stop all services
	docker-compose down

.PHONY: restart
restart: down up ## Restart all services

.PHONY: logs
logs: ## Show logs from all services
	docker-compose logs -f

.PHONY: test
test: test-backend ## Run all tests

.PHONY: test-backend
test-backend: ## Run backend tests
	cd backend && pytest tests/ -v --cov=app

.PHONY: test-frontend
test-frontend: ## Run frontend tests
	cd frontend && npm test

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests
	cd frontend && npm run test:e2e

.PHONY: lint
lint: lint-backend ## Run all linters

.PHONY: lint-backend
lint-backend: ## Lint backend code
	cd backend && ruff check .
	cd backend && black --check .
	cd backend && mypy . --ignore-missing-imports

.PHONY: lint-frontend
lint-frontend: ## Lint frontend code
	cd frontend && npm run lint

.PHONY: format
format: format-backend ## Format all code

.PHONY: format-backend
format-backend: ## Format backend code
	cd backend && black .
	cd backend && ruff check --fix .
	cd backend && isort .

.PHONY: format-frontend
format-frontend: ## Format frontend code
	cd frontend && npm run format

.PHONY: clean
clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

.PHONY: db-migrate
db-migrate: ## Run database migrations
	docker-compose exec backend alembic upgrade head

.PHONY: db-rollback
db-rollback: ## Rollback database migration
	docker-compose exec backend alembic downgrade -1

.PHONY: shell
shell: ## Open backend shell
	docker-compose exec backend /bin/bash

.PHONY: psql
psql: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U user -d ossgameforge

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	pre-commit run --all-files

.PHONY: security
security: ## Run security checks
	cd backend && bandit -r app/
	cd backend && safety check

.PHONY: demo
demo: ## Run demo mode
	./run_demo.sh