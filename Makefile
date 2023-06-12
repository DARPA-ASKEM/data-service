SHELL = /bin/bash
LANG = en_US.utf-8
PYTHON = $(shell which python3 || which python)
export LANG

SQL_HASH_FILE = data/.version
SCHEMA_SQL_FILE = data/001_schema.sql
DATA_SQL_FILE = data/002_data.sql

SCHEMA_FILES = $(shell find tds/schema/ tds/autogen/ -type f -name '*.py')
DATA_PY_FILES = $(shell find scripts/ -type f -name '*.py') 
DATA_FILES = $(DATA_PY_FILES) $(SCHEMA_SQL_FILE)
SQL_HASH = $(shell md5sum $(SCHEMA_FILES) $(DATA_PY_FILES) | md5sum | cut -c -32)

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
	mkdir -p "data/${S3_BUCKET}"
	docker compose --env-file api.env up --build -d;
	
.PHONY: gen-migration
gen-migration:
	poetry run model-build generate ./askem.dbml ./tds/autogen
	poetry run alembic -c migrate/alembic.ini check && ( \
	    echo "No migration needed" \
	) || ( \
		poetry run alembic -c migrate/alembic.ini revision --autogenerate -m "$$(date -u +'%Y%m%d%H%M%S')"; \
		poetry run alembic -c migrate/alembic.ini upgrade head; \
		make repopulate-db; \
	)

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

.PHONY:db-tag
db-tag: 
	echo '$(SQL_HASH)' > $(SQL_HASH_FILE);

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
