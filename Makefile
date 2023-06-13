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
	poetry run pylint ./tds
	poetry run pylint ./migrate
	poetry run pytest

.PHONY:up
up:
	docker compose --env-file api.env up -d;

.PHONY:build
build:
	docker compose --env-file api.env up --build -d;
	
.PHONY: gen-migration
gen-migration:
	docker compose --env-file api.env exec api bash -c "alembic -c migrate/alembic.ini revision -m \"${message}\""

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

.PHONY:db-full
db-full: | $(SCHEMA_SQL_FILE) $(DATA_SQL_FILE)

.PHONY:repopulate-db
repopulate-db:
	# Check if we need to rebuild the .sql files by checking if any prerequisite files are newer than the .sql files
	if [ "$(SQL_HASH)" != "$$(cat $(SQL_HASH_FILE))" ]; then \
		make down; \
		make db-clean; \
		NEO4J_ENABLED=False make up && \
		sleep 1 && \
		NEO4J_ENABLED=False make populate && \
		make db-full && \
		echo '$(SQL_HASH)' > $(SQL_HASH_FILE); \
	fi
