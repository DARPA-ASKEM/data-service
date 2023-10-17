SHELL = /bin/bash
LANG = en_US.utf-8
PYTHON = $(shell which python3 || which python)
export LANG

SCHEMA_FILES = $(shell find tds/schema/ tds/autogen/ -type f -name '*.py')
DATA_PY_FILES = $(shell find scripts/ -type f -name '*.py')
DOCKER_COMPOSE_FILE = ./docker/docker-compose.yml
ENV_FILE=.env

S3_BUCKET := $(shell grep S3_BUCKET .env | cut -d '=' -f2)

.PHONY:init
init:
	cp env.sample .env
	poetry install;
	poetry run pre-commit install
	
.PHONY:tidy
tidy: 
	poetry run pre-commit run;
	poetry run pylint ./tds ./migrations

.PHONY:test
test: 
	poetry run pytest

.PHONY:up
up:
	docker compose --file $(DOCKER_COMPOSE_FILE) --env-file $(ENV_FILE) up -d;

.PHONY:build
build:
	docker compose --file $(DOCKER_COMPOSE_FILE) --env-file $(ENV_FILE) up --build -d;
	
.PHONY: gen-migration
gen-migration:
	@echo -n -e "\\nEnter a description of the migration: "; \
	read message; \
	docker compose --file $(DOCKER_COMPOSE_FILE) --env-file $(ENV_FILE) exec -u $${UID} api alembic -c migrations/alembic.ini revision --autogenerate -m "$${message:-$$(date -u +'%Y%m%d%H%M%S')}" | \
	sed 's|/api/||'


.PHONY: run-migrations
run-migrations:
	docker compose --file $(DOCKER_COMPOSE_FILE) --env-file $(ENV_FILE) build migrations --no-cache;
	docker compose --file $(DOCKER_COMPOSE_FILE) --env-file $(ENV_FILE) start migrations;

.PHONY:populate
populate:up
	poetry run python3 scripts/upload_demo_data.py || (sleep 3; docker compose logs api; false);

.PHONY:fake
fake:up
	poetry run python3 scripts/upload_demo_data.py --fake
	
.PHONY:down
down:
	docker compose --file $(DOCKER_COMPOSE_FILE) down;

.PHONY:db-clean
db-clean:
	docker volume rm data-service_elasticsearch_data data-service_kibanadata data-service_tds_data data-service_neo4j_data

.PHONY:repopulate-db
repopulate-db:
	# Check if we need to rebuild the .sql files by checking if any prerequisite files are newer than the .sql files
	make down; \
	make db-clean; \
	SEED_DATA=true make up
