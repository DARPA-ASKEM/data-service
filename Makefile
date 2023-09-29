SHELL = /bin/bash
LANG = en_US.utf-8
PYTHON = $(shell which python3 || which python)
export LANG

SCHEMA_FILES = $(shell find tds/schema/ tds/autogen/ -type f -name '*.py')
DATA_PY_FILES = $(shell find scripts/ -type f -name '*.py')

S3_BUCKET := $(shell grep S3_BUCKET api.env | cut -d '=' -f2)

.PHONY:init
init:
	cp api.env.sample api.env
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
	docker compose --env-file api.env up -d;

.PHONY:build
build:
	docker compose --env-file api.env up --build -d;
	
.PHONY: gen-migration
gen-migration:
	@echo -n -e "\\nEnter a description of the migration: "; \
	read message; \
	docker compose --env-file api.env exec -u $${UID} api alembic -c migrations/alembic.ini revision -m "$${message:-$$(date -u +'%Y%m%d%H%M%S')}" | \
	sed 's|/api/||'


.PHONY: run-migrations
run-migrations:
	docker compose --env-file api.env build migrations --no-cache;
	docker compose --env-file api.env start migrations;

.PHONY:populate
populate:up
	poetry run python3 scripts/upload_demo_data.py || (sleep 3; docker compose logs api; false);

.PHONY:fake
fake:up
	poetry run python3 scripts/upload_demo_data.py --fake
	
.PHONY:down
down:
	docker compose --env-file api.env down;

.PHONY:db-clean
db-clean:
	docker volume rm data-service_elasticsearch_data data-service_kibanadata data-service_tds_data data-service_neo4j_data

.PHONY:repopulate-db
repopulate-db:
	# Check if we need to rebuild the .sql files by checking if any prerequisite files are newer than the .sql files
	make down; \
	make db-clean; \
	SEED_DATA=true make up
